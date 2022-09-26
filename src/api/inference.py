import uuid
from datetime import datetime

import cv2
import numpy as np
import torch
from fastapi import APIRouter, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse

from constants import MODEL_INFO
from models import SwinIR
from settings import model_settings
from utils import clear_memory


router = APIRouter()


@router.post("/upscale", response_model=str)
async def post_generation(request: Request, file: UploadFile):
    now = datetime.utcnow().timestamp()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    if file.content_type == "image/png":
        with open(f"{task_id}.png", "wb") as f:
            contents = await file.read()
            f.write(contents)
    else:
        raise HTTPException(status_code=400, detail="Only Support PNG file")
    model: SwinIR = request.app.state.model
    window_size = 8
    scale = MODEL_INFO[model_settings.model_name].scale
    img_lq = img_lq = cv2.imread(f"{task_id}.png", cv2.IMREAD_COLOR).astype(np.float32) / 255.0
    img_lq = np.transpose(img_lq if img_lq.shape[2] == 1 else img_lq[:, :, [2, 1, 0]], (2, 0, 1))  # HCW-BGR to CHW-RGB
    img_lq = torch.from_numpy(img_lq).float().unsqueeze(0).to(model_settings.device)  # CHW-RGB to NCHW-RGB
    # inference
    with torch.no_grad():
        # pad input image to be a multiple of window_size
        _, _, h_old, w_old = img_lq.size()
        h_pad = (h_old // window_size + 1) * window_size - h_old
        w_pad = (w_old // window_size + 1) * window_size - w_old
        img_lq = torch.cat([img_lq, torch.flip(img_lq, [2])], 2)[:, :, : h_old + h_pad, :]
        img_lq = torch.cat([img_lq, torch.flip(img_lq, [3])], 3)[:, :, :, : w_old + w_pad]
        output = model(img_lq)
        output = output[..., : h_old * scale, : w_old * scale]

    # save image
    output = output.data.squeeze().float().cpu().clamp_(0, 1).numpy()
    if output.ndim == 3:
        output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))  # CHW-RGB to HCW-BGR
    output = (output * 255.0).round().astype(np.uint8)  # float32 to uint8
    cv2.imwrite(f"{task_id}_SwinIR.png", output)
    clear_memory()
    return FileResponse(path=f"{task_id}_SwinIR.png")
