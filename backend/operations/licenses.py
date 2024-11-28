from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from models import Licenses, LicenseCreateRequest
import io

def add_license(db: Session, pilot_id: int, license_data: LicenseCreateRequest, license_file: UploadFile):
    """
    파일럿의 새로운 라이선스를 추가합니다.
    """
    # PDF 파일 처리
    if license_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")
    file_data = license_file.file.read()

    # 새로운 라이선스 추가
    new_license = Licenses(
        pilot_id=pilot_id,
        license_number=license_data.license_number,
        license_expiry_date=license_data.license_expiry_date,
        license_document=file_data,
        license_status="갱신 중",
    )
    
    db.add(new_license)
    db.commit()
    db.refresh(new_license)
    return new_license

def update_license_status(db: Session, license_id: int, new_status: str):
    """
    라이선스 상태를 업데이트합니다 ("허가", "갱신 중", "만료").
    """
    license = db.query(Licenses).filter(Licenses.license_id == license_id).first()
    if not license:
        raise HTTPException(status_code=404, detail="라이선스를 찾을 수 없습니다.")

    # 파일럿당 하나의 "허가" 상태만 허용 -> 이건 관리자의 권한인가 아니면 강제로 막아야 하는가
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