# Sandy Roofing Pros — Site Setup & Deployment Guide

Local lead generation site built with [Astro](https://astro.build) targeting homeowners in Sandy, Utah and Salt Lake County needing emergency roof repair.

**Domain:** sandyroofingpros.com  
**Phone:** (801) 555-0100 ← replace with your real CallRail number before going live

---

## Before You Deploy: Checklist

- [ ] Replace `(801) 555-0100` with your real CallRail number (see "Updating the Phone Number" below)
- [ ] Set up a form backend and replace the Formspree placeholder (see "Setting Up the Lead Form" below)
- [ ] Push the repo to GitHub
- [ ] Enable GitHub Pages with GitHub Actions as the source
- [ ] If using a custom domain, add it in GitHub Pages settings

---

## Step 1 — Install Dependencies Locally

Before deploying, install the project dependencies and verify the build works on your machine.

**Requirements:** [Node.js](https://nodejs.org) version 18 or higher.

Open a terminal in this project folder and run:

```bash
npm install
```

To preview the site locally:

```bash
npm run dev
```

This starts a local server at `http://localhost:4321`. Open that URL in your browser to see the site.

To test the production build locally:

```bash
npm run build
npm run preview
```

---

## Step 2 — Push to GitHub

### If this project is not yet on GitHub:

1. Go to [github.com](https://github.com) and sign in (or create a free account).
2. Click the **+** button in the top-right corner → **New repository**.
3. Name it something like `sandy-roofing-pros`.
4. Set it to **Private** (recommended — you don't need competitors seeing your project files).
5. Leave all other options at their defaults and click **Create repository**.

GitHub will show you a page with setup instructions. Since this project already has a git repo (the `.git` folder), use the **"push an existing repository"** commands it shows. They will look like this:

```bash
git remote add origin https://github.com/YOUR-USERNAME/sandy-roofing-pros.git
git branch -M main
git push -u origin main
```

> **Note:** This project is currently on the `master` branch. The command `git branch -M main` renames it to `main`, which is what GitHub and the deploy workflow expect. Run all three commands in order.

### If the repo is already on GitHub:

Just push your latest changes:

```bash
git add .
git commit -m "Initial Astro site"
git push
```

---

## Step 3 — Enable GitHub Pages

1. On GitHub, go to your repository page.
2. Click the **Settings** tab (near the top of the repo page).
3. In the left sidebar, click **Pages**.
4. Under **Build and deployment**, find the **Source** dropdown.
5. Change it from "Deploy from a branch" to **GitHub Actions**.
6. Click **Save**.

That's it. GitHub Pages is now configured to receive deployments from the Actions workflow included in this project (`.github/workflows/deploy.yml`).

### Trigger the First Deploy

The workflow runs automatically every time you push to `main`. To trigger it manually right now:

1. Click the **Actions** tab on your GitHub repo page.
2. Click **Deploy to GitHub Pages** in the left sidebar.
3. Click the **Run workflow** button → **Run workflow**.

Watch the workflow run. When both the `build` and `deploy` jobs show a green checkmark, your site is live.

---

## Step 4 — Connect Your Custom Domain

If you want the site to be live at `sandyroofingpros.com` (instead of `your-username.github.io/sandy-roofing-pros`):

### In GitHub:

1. Go to **Settings → Pages** in your repository.
2. Under **Custom domain**, type `sandyroofingpros.com` and click **Save**.
3. Check the **Enforce HTTPS** checkbox (may take a few minutes to appear after the domain is verified).

### At Your Domain Registrar (e.g., GoDaddy, Namecheap, Google Domains):

You need to point your domain's DNS to GitHub's servers. Add these DNS records:

**Option A — Apex domain (sandyroofingpros.com):**

Add four `A` records pointing to these GitHub IPs:

| Type | Name | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

Also add a `CNAME` record for the `www` subdomain:

| Type | Name | Value |
|------|------|-------|
| CNAME | www | your-username.github.io |

**Option B — Add both apex and www:**

Set up the A records above AND add `www` as a CNAME pointing to `your-username.github.io`.

> DNS changes can take anywhere from a few minutes to 48 hours to fully propagate. Once they do, GitHub will automatically provision a free SSL certificate (HTTPS) for your domain.

### The CNAME File

This project already has a `public/CNAME` file containing `sandyroofingpros.com`. Astro copies this file into the `dist/` folder during build, which tells GitHub Pages your custom domain. You do not need to create or edit this file.

---

## Updating the Phone Number

The phone number appears in three places. Do a find-and-replace across the project before going live:

**Find:** `(801) 555-0100`  
**Replace with:** your real CallRail number (e.g., `(801) 555-1234`)

**Also update the `tel:` href:**  
**Find:** `tel:+18015550100`  
**Replace with:** your real number in E.164 format (e.g., `tel:+18015551234`)

Files that contain the phone number:
- `src/components/Header.astro`
- `src/components/Footer.astro`
- `src/pages/services.astro`
- `src/pages/contact.astro`
- `src/layouts/BaseLayout.astro` (schema markup)

---

## Setting Up the Lead Form

The lead forms on the Home and Contact pages submit to Formspree by default. Formspree is a free service that emails form submissions to you — no backend server required.

### Setup (free):

1. Go to [formspree.io](https://formspree.io) and create a free account.
2. Click **New Form**, give it a name like "Sandy Roofing Pros Lead Form".
3. Copy the form endpoint — it looks like: `https://formspree.io/f/abcdefgh`
4. Open `src/components/LeadForm.astro`.
5. Find this line:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```
6. Replace `YOUR_FORM_ID` with your actual Formspree form ID (the part after `/f/`).
7. In Formspree, set the notification email to wherever you want leads delivered.

That's it — form submissions will be emailed to you instantly.

### Alternatives to Formspree:

- **[Getform.io](https://getform.io)** — similar to Formspree, generous free tier
- **[Web3Forms](https://web3forms.com)** — free, no account required
- **[Netlify Forms](https://www.netlify.com/products/forms/)** — works automatically if you deploy to Netlify instead of GitHub Pages

---

## Project Structure

```
/
├── public/
│   ├── CNAME              ← Custom domain file (do not delete)
│   ├── favicon.svg
│   └── robots.txt
├── src/
│   ├── components/
│   │   ├── Header.astro   ← Sticky header with phone + CTA
│   │   ├── Footer.astro   ← Footer with disclaimer
│   │   └── LeadForm.astro ← Reusable lead capture form
│   ├── layouts/
│   │   └── BaseLayout.astro ← Head, schema markup, global layout
│   ├── pages/
│   │   ├── index.astro       ← Homepage
│   │   ├── services.astro    ← Services page
│   │   ├── service-area.astro← Service Area page
│   │   └── contact.astro     ← Contact page
│   └── styles/
│       └── global.css        ← All site styles
├── .github/
│   └── workflows/
│       └── deploy.yml     ← GitHub Actions deploy workflow
├── astro.config.mjs
└── package.json
```

---

## Making Changes After Deployment

Whenever you edit any file and push to GitHub, the site rebuilds and deploys automatically. The full deploy takes about 60–90 seconds.

```bash
# After making edits:
git add .
git commit -m "describe your change here"
git push
```

Then check the **Actions** tab on GitHub to watch the deploy complete.

---

## Design Pass (Next Step)

This initial build focuses on content, structure, and SEO. When you're ready to apply a visual design:

- All styles live in `src/styles/global.css` — edit CSS variables at the top of that file to change the color scheme globally
- The primary color is `--color-primary: #B91C1C` (dark red)
- Consider adding [Tailwind CSS](https://docs.astro.build/en/guides/integrations-guide/tailwind/) via `npx astro add tailwind` for the design pass
