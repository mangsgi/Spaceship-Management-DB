from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from models import Licenses, LicenseResponse, LicenseCreateRequest
from datetime import date
import json

# Pilot - 파일럿의 새로운 라이선스 추가
async def add_license(db: Session, license_data: UploadFile, license_file: UploadFile):
    # PDF 파일 처리
    if license_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")
    file_data = license_file.file.read()

    try:
        license_data_content = await license_data.read()
        parsed_data = json.loads(license_data_content)
        license_request = LicenseCreateRequest(**parsed_data)  # JSON → Pydantic 모델
    except json.JSONDecodeError:
        raise HTTPException(status_code=401, detail="JSON 파일만 업로드 가능합니다.")
    except ValueError as e:
        raise HTTPException(status_code=402, detail=f"유효하지 않은 License data: {str(e)}")

    # 새로운 라이선스 추가
    new_license = Licenses(
        pilot_id = license_request.pilot_id,
        license_number = license_request.license_number,
        license_expiry_date = license_request.license_expiry_date,
        license_document=file_data,
        license_status="갱신 중",
    )
    
    db.add(new_license)
    db.commit()
    db.refresh(new_license)
    return LicenseResponse.model_validate(new_license)

# Fin Administartor - 라이선스 상태 변경
def update_license_status(db: Session, license_id: int, new_status: str):
    license = db.query(Licenses).filter(Licenses.license_id == license_id).first()
    if not license:
        raise HTTPException(status_code=404, detail="라이선스를 찾을 수 없습니다.")

    # 파일럿당 하나의 "허가" 상태만 허용 -> TODO 이건 관리자의 권한인가 아니면 강제로 막아야 하는가
    if new_status == "허가":
        existing_approved = (
            db.query(Licenses)
            .filter(Licenses.pilot_id == license.pilot_id, Licenses.license_status == "허가")
            .first()
        )
        if existing_approved:
            raise HTTPException(
                status_code=400, detail="파일럿당 하나의 '허가' 상태 라이선스만 허용됩니다."
            )

    # 상태 업데이트
    license.license_status = new_status
    db.commit()
    db.refresh(license)
    return license