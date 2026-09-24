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

**Change the navigation or footer.** Each page carries its own copy of the header and footer, so make the same edit in every `.html` file.

## Custom domain (optional)

A domain such as `bhushanlab.org` typically costs about $10–20 a year to register. The site works fine without one. If you add one, enter it under **Settings → Pages → Custom domain**.
