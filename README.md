# Bhushan Research Group website

Plain HTML and CSS, published free with GitHub Pages at https://bhushan-group.github.io. No build step, no plugins, no cost.

## Update the site

Open any file on github.com in the `bhushan-group.github.io` repository, click the pencil icon, make the change, and click **Commit changes**. The live site updates within a couple of minutes.

To replace several files at once, open the repository, click **Add file → Upload files**, drag the files in, and click **Commit changes**. Files with the same name are replaced; everything else is left alone.

## Lab news

News lives in one file, `data/news.json`. The homepage shows the eight newest items in a strip visitors can scroll sideways, and the News page shows everything, grouped by year, with buttons to filter by type and jump to a year. The order inside the file doesn't matter; the site sorts by date.

Each item has a date, a type (Paper, Talk, Award, People, Grant, Event, Media or Lab), a headline, and optionally a sentence or two, a photo and a link. Items without a photo show a colored icon for their type.

### Post news with the form (recommended)

Pages CMS is a free editor that turns the news file into a form. It saves straight into the repository, so every change is recorded and can be undone.

1. Go to https://app.pagescms.org and sign in with GitHub.
2. Install the Pages CMS GitHub App on the `bhushan-group` organization and give it access to the `bhushan-group.github.io` repository.
3. Open the repository and choose **Lab news**. Click **Add an item**, fill in the fields, switch on **Show on website**, and save.

### Let students post news

1. In Pages CMS, open the repository's **Collaborators** settings and invite each student by email. They don't need a GitHub account.
2. The student gets an email, signs in, and sees only the **Lab news** form and the news photo folder. They can't change any other part of the site.
3. New items start with **Show on website** switched off, so a student's post is saved but stays hidden. Read it in the same form, fix anything you like, and switch **Show on website** on. It appears on the site within a couple of minutes.
4. Every save is recorded in the repository's history under the student's name. To undo one, open **Commits** on GitHub, or simply edit or delete the item in the form.

Ask students to let you know when they've posted, since Pages CMS doesn't send notifications. Remove a collaborator from the same settings page when they leave the lab.

The form is defined in `.pages.yml` at the top of the repository. Files whose names start with a dot are hidden on Macs and can be skipped when you drag a folder into GitHub. If `.pages.yml` is missing from the repository, create it on GitHub with **Add file → Create new file**, name it `.pages.yml`, and paste in the contents of the copy in this folder.

### Edit the news file by hand

Open `data/news.json` on GitHub, click the pencil, and copy an existing entry from `{` to `}`. Entries are separated by commas, with no comma after the last one. If the news section disappears from the homepage after a save, a missing or extra comma is the usual cause. Items added by hand appear unless they contain `"show": false`.

Dates are written `2026-09-24`, or `2026-09` or `2026` when the exact day doesn't matter. An item with only a year is listed after the dated items of that year. To start a new line inside the text (for a list of talks, say), press Enter in the form or type `\n` when editing the file by hand.

## Photos

Site photos are in `assets/img/photos/`. To swap one, upload a new JPG with exactly the same file name; it replaces the old one everywhere it's used. Landscape images at least 1200 pixels wide look sharpest. News photos uploaded through the form go in `assets/img/news/`.

Only post photos that everyone in them is happy to have online.

## Common updates

**Add a publication.** In `publications.html`, copy one `<li class="pub"> … </li>` block, paste it at the top of the list, and change the year, title, link, authors and journal. If the paper belongs to a research theme, paste the same block into that theme's "Selected papers" list in `research.html`. To feature it on the homepage, replace one of the three blocks under "Recent publications" in `index.html`. Consider posting it as news too.

**Add a person.** In `people.html`, copy one `<article class="person"> … </article>` block into the right group (staff, graduate, undergraduate) and change the initials, name, role and bio. Delete the block when someone leaves.

**Add a headshot.** Upload a square JPG (about 400 × 400 pixels) to `assets/img/people/`. In `people.html`, replace that person's initials line

    <span class="avatar avatar-sm" aria-hidden="true">ID</span>

with

    <span class="avatar avatar-sm"><img src="assets/img/people/ishita-dasgupta.jpg" alt=""></span>

For the PI photo, do the same with the `avatar avatar-lg` line.

**Add a Google Scholar link.** In `index.html`, find `All publications` and add after it:

    <a class="text-link" href="YOUR-SCHOLAR-URL">Google Scholar profile</a>

**Change colors.** At the top of `assets/css/style.css`: `--deep` is the dark teal of the page headers, `--wine` the Join band, `--teal` and `--scarlet` the accents, and `--tint-teal`, `--tint-rose` and `--tint-sand` the soft card backgrounds.

**Change the navigation or footer.** Each page carries its own copy of the header and footer, so make the same edit in every `.html` file.

## Custom domain (optional)

A domain such as `bhushanlab.org` typically costs about $10–20 a year to register. The site works fine without one. If you add one, enter it under **Settings → Pages → Custom domain**.
