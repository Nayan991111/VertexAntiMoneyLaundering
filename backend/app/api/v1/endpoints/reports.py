from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from app.services.report_service import report_service  # Singleton Instance
from app.services.graph_service import graph_service
from app.api.deps import get_current_user  # <--- SECURITY: Import Auth Dependency
import os

router = APIRouter()

@router.post("/generate_sar/{ring_index}")
async def generate_sar(
    ring_index: int, 
    current_user: str = Depends(get_current_user) # <--- SECURITY: Lock the door
):
    """
    Generates a Suspicious Activity Report (SAR) PDF for a specific Money Laundering Ring.
    SECURE: Requires valid JWT Token.
    """
    # 0. Security Audit Log (Internal console log)
    print(f"[SECURITY AUDIT] User '{current_user}' is requesting SAR generation for Ring #{ring_index}")

    # 1. Fetch Ring Data from Graph Service
    rings = graph_service.detect_circular_flow()
    
    # Validation: Ensure rings exist
    if not rings:
        raise HTTPException(status_code=404, detail="No money laundering rings detected to report.")
        
    # Validation: Ensure index is valid
    if ring_index < 0 or ring_index >= len(rings):
        raise HTTPException(status_code=404, detail=f"Ring index {ring_index} not found. Available rings: {len(rings)}.")
    
    target_ring = rings[ring_index]
    
    # 2. Generate PDF using the Report Service
    try:
        # Create a unique Case ID (Appended with User Identity for Audit)
        case_id = f"CASE-{ring_index + 101}-OFFICER-{current_user}"
        
        # Generate the file and get the path
        file_path = report_service.generate_sar_pdf(case_id, target_ring)
        
        # 3. Return the File
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path, 
                filename=os.path.basename(file_path),
                media_type='application/pdf'
            )
        else:
            raise HTTPException(status_code=500, detail="PDF file was not created successfully.")
            
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))