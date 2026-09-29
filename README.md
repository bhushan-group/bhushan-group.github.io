# Bhushan Research Group website

Plain HTML and CSS. No build step, no plugins, no cost. It runs on GitHub Pages or any web host.

## Put the site online (GitHub Pages)

1. Sign up for a free account at github.com.
2. Create a free organization for the lab so the site isn't tied to one person's account: click your profile picture → **Your organizations** → **New organization** → **Free**. Pick a name such as `bhushanlab`.
3. In the organization, click **New repository**. Name it exactly `bhushanlab.github.io` (your organization name followed by `.github.io`). Set it to **Public**. Leave "Add a README" unchecked. Click **Create repository**.
4. On the empty repository page, click **uploading an existing file**. On your computer, unzip the download and open the `bhushan-lab-site` folder. Select everything inside it (not the folder itself) and drag it into the browser window. Click **Commit changes**.
5. Go to **Settings → Pages**. Under **Build and deployment**, set Source to **Deploy from a branch**, Branch to **main**, and folder to **/ (root)**. Click **Save**. For repositories named `<name>.github.io` this is often already set.
6. After a minute or two the site is live at `https://bhushanlab.github.io`. The Actions tab shows progress if it takes longer.

Then link the new address from your Illinois Tech faculty profile and the department page, and add a "This site has moved" link at the top of the old Google Site.

## Edit the site from the browser

Open any file on github.com, click the pencil icon, make the change, and click **Commit changes**. The live site updates within a couple of minutes.

To let students edit, add them to the organization (**People → Invite member**).

## Lab news

News lives in one file, `data/news.json`. The homepage shows the three newest items and the News page shows them all, grouped by year. The order inside the file doesn't matter; the site sorts by date.

**With a form (recommended).** Pages CMS turns the news file into a simple form.

1. Go to https://app.pagescms.org and sign in with GitHub.
2. Install the Pages CMS GitHub App on the `bhushan-group` organization and give it access to the `bhushan-group.github.io` repository.
3. Open the repository and choose **Lab news**. Add an item, fill in the date, headline, details and link, and save. The site updates within a couple of minutes.
4. To let students post news without a GitHub account, invite them as collaborators by email from Pages CMS.

The form is defined in `.pages.yml` at the top of the repository. Files whose names start with a dot are hidden on Macs and can be skipped when you drag a folder into GitHub. If `.pages.yml` is missing from the repository, create it on GitHub with **Add file → Create new file**, name it `.pages.yml`, and paste in the contents of the copy in this folder.

**By hand.** Open `data/news.json` on GitHub, click the pencil, and copy an existing entry from `{` to `}`. Entries are separated by commas, with no comma after the last one. If the news section disappears from the homepage after a save, a missing or extra comma is the usual cause.

Dates are written `2026-09-24`, or `2026-09` or `2026` when the exact day doesn't matter.

## Common updates

**Add a publication.** In `publications.html`, copy one `<li class="pub"> … </li>` block, paste it at the top of the list, and change the year, title, link, authors and journal. If the paper belongs to a research theme, paste the same block into that theme's "Selected papers" list in `research.html`. To feature it on the homepage, replace one of the three blocks under "Recent publications" in `index.html`.

**Add a person.** In `people.html`, copy one `<article class="person"> … </article>` block into the right group (staff, graduate, undergraduate) and change the initials, name, role and bio. Delete the block when someone leaves.

**Add a photo.** Upload a square JPG (about 400 × 400 pixels) to `assets/img/people/`. In `people.html`, replace that person's initials line

    <span class="avatar avatar-sm" aria-hidden="true">ID</span>

with

    <span class="avatar avatar-sm"><img src="assets/img/people/ishita-dasgupta.jpg" alt=""></span>

For the PI photo, do the same with the `avatar avatar-lg` line.

**Add a Google Scholar link.** In `index.html`, find `All publications` and add after it:

    <a class="text-link" href="YOUR-SCHOLAR-URL">Google Scholar profile</a>

**Change colors.** At the top of `assets/css/style.css`, `--accent` is the red and `--flow` is the teal.

**Change the navigation or footer.** Each page carries its own copy of the header and footer, so make the same edit in every `.html` file, including `news.html`.

## Custom domain (optional)

A domain such as `bhushanlab.org` typically costs about $10–20 a year to register. The site works fine without one. If you add one, enter it under **Settings → Pages → Custom domain**.
