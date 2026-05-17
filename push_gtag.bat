@echo off
cd /d "C:\Users\jacks\OneDrive\Documents\Claude\Projects\Project Launch- SLC Metro Roofing (1)"
echo Adding files...
git add src/layouts/BaseLayout.astro src/components/LeadForm.astro
echo Committing...
git commit -m "Add Google Ads conversion tracking (AW-18149105122)"
echo Pushing to GitHub...
git push origin main
echo.
echo Done! GitHub Actions will deploy in ~2 minutes.
pause
