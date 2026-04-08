import base64
import json

from fastapi import HTTPException


ENCODED_QUIZ_DATA = (
    "eyJzZXNzaW9uIjp7ImlkIjoxLCJ0aXRsZSI6IkJhY2tlbmQgU2Vzc2lvbiBXYXJtdXAiLCJkZXNjcmlwdGlvbiI6IjE1IHdvcmtzaG9wIHF1ZXN0aW9ucyBvbiBETlMsIEhUVFBTLCBIVFRQIG1ldGhvZHMsIEFQSXMsIGFuZCBiYWNrZW5kIGZ1bmRhbWVudGFscy4iLCJ0b3BpYyI6IkJhY2tlbmQgQmFzaWNzIn0sInF1ZXN0aW9ucyI6W3sicG9zaXRpb24iOjEsInF1ZXN0aW9uIjoiV2hhdCBkb2VzIEROUyBtYWlubHkgZG8gb24gdGhlIGludGVybmV0PyIsIm9wdGlvbnMiOnsiQSI6IkVuY3J5cHQgdGhlIGRhdGEgYmV0d2VlbiB0aGUgYnJvd3NlciBhbmQgdGhlIHNlcnZlciIsIkIiOiJUcmFuc2xhdGUgYSBkb21haW4gbmFtZSBpbnRvIGFuIElQIGFkZHJlc3MiLCJDIjoiU3RvcmUgZnJvbnRlbmQgZmlsZXMgaW4gdGhlIGJyb3dzZXIgY2FjaGUiLCJEIjoiQ3JlYXRlIGRhdGFiYXNlIHRhYmxlcyBmb3IgYW4gYXBwbGljYXRpb24ifSwiY29ycmVjdF9vcHRpb24iOiJCIn0seyJwb3NpdGlvbiI6MiwicXVlc3Rpb24iOiJXaGljaCBwcm90b2NvbCBpcyBjb21tb25seSB1c2VkIHRvIGxvYWQgYSBzZWN1cmUgd2Vic2l0ZT8iLCJvcHRpb25zIjp7IkEiOiJGVFAiLCJCIjoiU01UUCIsIkMiOiJIVFRQUyIsIkQiOiJTU0gifSwiY29ycmVjdF9vcHRpb24iOiJDIn0seyJwb3NpdGlvbiI6MywicXVlc3Rpb24iOiJXaGF0IGlzIHRoZSBtYWluIHB1cnBvc2Ugb2YgSFRUUFM/Iiwib3B0aW9ucyI6eyJBIjoiVG8gY29tcHJlc3MgSlNPTiByZXNwb25zZXMiLCJCIjoiVG8gbWFrZSBhIHNpdGUgZmFzdGVyIHRoYW4gYWxsIEhUVFAgcmVxdWVzdHMiLCJDIjoiVG8gc2VjdXJlIGNvbW11bmljYXRpb24gd2l0aCBlbmNyeXB0aW9uIGFuZCBjZXJ0aWZpY2F0ZSB2YWxpZGF0aW9uIiwiRCI6IlRvIHJlcGxhY2UgRE5TIHJlY29yZHMifSwiY29ycmVjdF9vcHRpb24iOiJDIn0seyJwb3NpdGlvbiI6NCwicXVlc3Rpb24iOiJXaGljaCBIVFRQIG1ldGhvZCBpcyB1c3VhbGx5IHVzZWQgdG8gY3JlYXRlIGEgbmV3IHJlc291cmNlPyIsIm9wdGlvbnMiOnsiQSI6IkdFVCIsIkIiOiJQT1NUIiwiQyI6IkRFTEVURSIsIkQiOiJIRUFEIn0sImNvcnJlY3Rfb3B0aW9uIjoiQiJ9LHsicG9zaXRpb24iOjUsInF1ZXN0aW9uIjoiV2hpY2ggSFRUUCBtZXRob2Qgc2hvdWxkIGJlIHVzZWQgdG8gZmV0Y2ggZGF0YSB3aXRob3V0IGNoYW5naW5nIGl0PyIsIm9wdGlvbnMiOnsiQSI6IkdFVCIsIkIiOiJQQVRDSCIsIkMiOiJQVVQiLCJEIjoiREVMRVRFIn0sImNvcnJlY3Rfb3B0aW9uIjoiQSJ9LHsicG9zaXRpb24iOjYsInF1ZXN0aW9uIjoiV2hpY2ggSFRUUCBtZXRob2QgaXMgY29tbW9ubHkgdXNlZCB0byBmdWxseSByZXBsYWNlIGFuIGV4aXN0aW5nIHJlc291cmNlPyIsIm9wdGlvbnMiOnsiQSI6IlBVVCIsIkIiOiJUUkFDRSIsIkMiOiJPUFRJT05TIiwiRCI6IkNPTk5FQ1QifSwiY29ycmVjdF9vcHRpb24iOiJBIn0seyJwb3NpdGlvbiI6NywicXVlc3Rpb24iOiJXaGljaCBIVFRQIG1ldGhvZCBpcyBjb21tb25seSB1c2VkIHRvIHBhcnRpYWxseSB1cGRhdGUgYSByZXNvdXJjZT8iLCJvcHRpb25zIjp7IkEiOiJQT1NUIiwiQiI6IlBBVENIIiwiQyI6IkdFVCIsIkQiOiJIRUFEIn0sImNvcnJlY3Rfb3B0aW9uIjoiQiJ9LHsicG9zaXRpb24iOjgsInF1ZXN0aW9uIjoiV2hhdCBkb2VzIGEgYDQwNGAgcmVzcG9uc2UgdXN1YWxseSBtZWFuPyIsIm9wdGlvbnMiOnsiQSI6IlRoZSB1c2VyIGlzIG5vdCBsb2dnZWQgaW4iLCJCIjoiVGhlIHNlcnZlciBjcmFzaGVkIGR1cmluZyBzdGFydHVwIiwiQyI6IlRoZSByZXF1ZXN0ZWQgcmVzb3VyY2Ugd2FzIG5vdCBmb3VuZCIsIkQiOiJUaGUgYnJvd3NlciBzZW50IGludmFsaWQgSlNPTiJ9LCJjb3JyZWN0X29wdGlvbiI6IkMifSx7InBvc2l0aW9uIjo5LCJxdWVzdGlvbiI6IldoYXQgZG9lcyBhIGA1MDBgIHJlc3BvbnNlIHVzdWFsbHkgbWVhbj8iLCJvcHRpb25zIjp7IkEiOiJUaGVyZSBpcyBhIHNlcnZlci1zaWRlIGVycm9yIiwiQiI6IlRoZSByZXF1ZXN0IHdhcyBzdWNjZXNzZnVsIiwiQyI6IlRoZSBjbGllbnQgbXVzdCBsb2cgaW4gYWdhaW4iLCJEIjoiVGhlIEROUyBsb29rdXAgZmFpbGVkIn0sImNvcnJlY3Rfb3B0aW9uIjoiQSJ9LHsicG9zaXRpb24iOjEwLCJxdWVzdGlvbiI6IldoeSBkbyBBUElzIGNvbW1vbmx5IHVzZSBKU09OPyIsIm9wdGlvbnMiOnsiQSI6Ikl0IGNhbiBvbmx5IGJlIHJlYWQgYnkgUHl0aG9uIHNlcnZlcnMiLCJCIjoiSXQgaXMgYSBsaWdodHdlaWdodCBmb3JtYXQgdGhhdCBpcyBlYXN5IGZvciBjbGllbnRzIGFuZCBzZXJ2ZXJzIHRvIGV4Y2hhbmdlIiwiQyI6Ikl0IGF1dG9tYXRpY2FsbHkgZW5jcnlwdHMgcGFzc3dvcmRzIiwiRCI6Ikl0IHJlcGxhY2VzIFNRTCBpbiBkYXRhYmFzZXMifSwiY29ycmVjdF9vcHRpb24iOiJCIn0seyJwb3NpdGlvbiI6MTEsInF1ZXN0aW9uIjoiV2hhdCBpcyBhbiBBUEkgZW5kcG9pbnQ/Iiwib3B0aW9ucyI6eyJBIjoiQSBDU1MgY2xhc3MgdXNlZCBieSBmcm9udGVuZCBwYWdlcyIsIkIiOiJBIHNwZWNpZmljIFVSTCBwYXRoIHdoZXJlIGEgYmFja2VuZCBleHBvc2VzIGEgcmVzb3VyY2Ugb3IgYWN0aW9uIiwiQyI6IkEgbG9jYWwgZGF0YWJhc2UgYmFja3VwIGZpbGUiLCJEIjoiQSBjb21tYW5kIHRoYXQgb25seSB3b3JrcyBpbiBTd2FnZ2VyIn0sImNvcnJlY3Rfb3B0aW9uIjoiQiJ9LHsicG9zaXRpb24iOjEyLCJxdWVzdGlvbiI6IldoYXQgaXMgdGhlIHJvbGUgb2YgYSBiYWNrZW5kIHNlcnZlciBpbiBhIHdlYiBhcHA/Iiwib3B0aW9ucyI6eyJBIjoiT25seSBkZXNpZ25pbmcgdGhlIHBhZ2UgY29sb3JzIiwiQiI6Ik9ubHkgcmVnaXN0ZXJpbmcgZG9tYWluIG5hbWVzIiwiQyI6IkhhbmRsaW5nIGJ1c2luZXNzIGxvZ2ljLCBkYXRhIHN0b3JhZ2UsIGFuZCBBUEkgcmVzcG9uc2VzIiwiRCI6IlJlcGxhY2luZyB0aGUgdXNlcidzIGJyb3dzZXIifSwiY29ycmVjdF9vcHRpb24iOiJDIn0seyJwb3NpdGlvbiI6MTMsInF1ZXN0aW9uIjoiV2hhdCBpcyB0aGUgbWFpbiBkaWZmZXJlbmNlIGJldHdlZW4gU1FMIGFuZCBOb1NRTCBkYXRhYmFzZXM/Iiwib3B0aW9ucyI6eyJBIjoiU1FMIHVzZXMgc3RydWN0dXJlZCB0YWJsZXMsIHdoaWxlIE5vU1FMIHVzZXMgZmxleGlibGUgZGF0YSBtb2RlbHMiLCJCIjoiU1FMIGlzIGZhc3RlciB0aGFuIE5vU1FMIGluIGFsbCBjYXNlcyIsIkMiOiJOb1NRTCBvbmx5IHdvcmtzIG9uIFdpbmRvd3MiLCJEIjoiU1FMIGNhbm5vdCBzdG9yZSBkYXRhIn0sImNvcnJlY3Rfb3B0aW9uIjoiQSJ9LHsicG9zaXRpb24iOjE0LCJxdWVzdGlvbiI6IldoeSBpcyB2YWxpZGF0aW9uIGltcG9ydGFudCBvbiB0aGUgYmFja2VuZD8iLCJvcHRpb25zIjp7IkEiOiJJdCBsZXRzIENTUyBsb2FkIGZhc3RlciIsIkIiOiJJdCBjaGVja3MgaW5jb21pbmcgZGF0YSBiZWZvcmUgdXNpbmcgb3Igc3RvcmluZyBpdCIsIkMiOiJJdCByZW1vdmVzIHRoZSBuZWVkIGZvciBhIGRhdGFiYXNlIiwiRCI6Ikl0IG1ha2VzIGV2ZXJ5IHJlcXVlc3QgaWRlbXBvdGVudCJ9LCJjb3JyZWN0X29wdGlvbiI6IkIifSx7InBvc2l0aW9uIjoxNSwicXVlc3Rpb24iOiJXaGF0IGlzIFN3YWdnZXIgbWFpbmx5IHVzZWZ1bCBmb3IgaW4gdGhpcyB3b3Jrc2hvcCBhcHA/Iiwib3B0aW9ucyI6eyJBIjoiV3JpdGluZyBTUUwgbWlncmF0aW9ucyBhdXRvbWF0aWNhbGx5IiwiQiI6Ikhvc3Rpbmcgc3RhdGljIEhUTUwgcGFnZXMiLCJDIjoiRXhwbG9yaW5nIGFuZCB0ZXN0aW5nIEFQSSBlbmRwb2ludHMgZnJvbSBnZW5lcmF0ZWQgZG9jdW1lbnRhdGlvbiIsIkQiOiJDcmVhdGluZyBTU0wgY2VydGlmaWNhdGVzIn0sImNvcnJlY3Rfb3B0aW9uIjoiQyJ9XX0="
)


def _load_quiz_data():
    raw = base64.b64decode(ENCODED_QUIZ_DATA.encode("ascii"))
    return json.loads(raw.decode("utf-8"))


_QUIZ_DATA = _load_quiz_data()
QUIZ_SESSION = _QUIZ_DATA["session"]
QUIZ_QUESTIONS = _QUIZ_DATA["questions"]


def get_quiz_session_or_404(session_id: int):
    if session_id != QUIZ_SESSION["id"]:
        raise HTTPException(status_code=404, detail="Quiz session not found")
    return {
        **QUIZ_SESSION,
        "question_count": len(QUIZ_QUESTIONS),
    }


def get_quiz_question_by_position_or_404(session_id: int, question_position: int):
    get_quiz_session_or_404(session_id)
    for item in QUIZ_QUESTIONS:
        if item["position"] == question_position:
            return {
                "position": item["position"],
                "question": item["question"],
                "options": [
                    {"key": "A", "text": item["options"]["A"]},
                    {"key": "B", "text": item["options"]["B"]},
                    {"key": "C", "text": item["options"]["C"]},
                    {"key": "D", "text": item["options"]["D"]},
                ],
            }
    raise HTTPException(status_code=404, detail="Quiz question not found")


def check_quiz_answer_or_404(session_id: int, question_position: int, selected_option: str):
    get_quiz_session_or_404(session_id)
    chosen = selected_option.strip().upper()
    if chosen not in {"A", "B", "C", "D"}:
        raise HTTPException(status_code=400, detail="selected_option must be one of A, B, C, D")

    for item in QUIZ_QUESTIONS:
        if item["position"] == question_position:
            return {
                "position": question_position,
                "correct": item["correct_option"] == chosen,
            }
    raise HTTPException(status_code=404, detail="Quiz question not found")
