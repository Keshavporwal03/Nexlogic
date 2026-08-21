## 2026-08-07 — Backend Completion & Logic Refinements
- Built: 
  - FastAPI server with Supabase DB models (`users`, `company`, `jobs`, `candidates`, etc.).
  - Candidate Search API with priority logic (LinkedIn -> GitHub fallback) and CSV upload with weighted scoring (Skills 40%, Experience 30%, Location 20%, Education 10%).
  - AI Banner Generator (Hugging Face `FLUX.1-schnell`) with Pillow logo/text overlay and a solid-color fallback mechanism.
  - AI Post Generator (Hugging Face `Mistral-7B-Instruct-v0.3`) with `better-profanity` safety filtering that regenerates once and then falls back to a template.
- Decisions confirmed with user:
  - Exact candidate match scoring is strictly enforced.
  - Profanity filter retry-and-template fallback logic over simple masking.
- Tests Run (Python 3.12 Environment):
  - Local virtual environment rebuilt successfully with standard Python 3.12.
  - Smoke test executed successfully: Swagger UI loads correctly on `/docs`, Banner Fallback generates default solid-background image as expected when Hugging Face API is mocked to fail, and Candidate Search API handles fallback requests gracefully. DB schema initializes successfully on server startup.
- Pending / known issues: none

## 2026-08-10 — V2 Richer Banner & Post Templates
- Built: 
  - Added new fields `apply_link`, `contact_email`, `why_join_us` to `company` and `jobs` tables in PostgreSQL.
  - Updated Pydantic schemas in backend to handle new fields.
  - Overhauled Banner Generator (`banner_gen.py`) layout: deterministic corner frames, table-layout for details, and Montserrat typography overlay using Pillow.
  - Overhauled Post Generator (`post_gen.py`) prompt: structured generation with strict formatting for hook, position details, company `why_join_us` highlights, apply links, and rich hashtags.
  - Downloaded Montserrat fonts (`Montserrat-Bold.ttf`, `Montserrat-Regular.ttf`) to backend `static/fonts` for deterministic text rendering.
  - Updated frontend `index.html` to load Montserrat from Google Fonts and `tailwind.config.js` to configure `font-heading`.
  - Added necessary state variables and inputs to `BannerGenerator.jsx` and `PostGenerator.jsx` to pass the new fields directly to AI endpoints.
- Decisions confirmed with user:
  - Addressed new UI inputs directly in the Generator pages for rapid testing/generation instead of a dedicated Company Profile page to minimize context switching, although backend supports DB-level reuse.
- Pending / known issues: none

## 2026-08-10 — Alembic & Company Profile UI
- Built:
  - Installed and configured `alembic` to track database migrations. Generated the first `baseline` migration to track the current Supabase PostgreSQL schema.
  - Added `CompanyProfile.jsx` to manage global default fields (`apply_link`, `contact_email`, `why_join_us`).
  - Implemented `/company/profile` API endpoints in `company.py` to persist these defaults.
  - Refactored `BannerGenerator` and `PostGenerator` to automatically fetch these company details from the backend, removing the redundant fields from the UI while keeping the job-specific `apply_link` override.
