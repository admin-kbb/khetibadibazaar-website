# Kheti Badi Bazaar website

A responsive, static introduction to the Kheti Badi Bazaar agricultural marketplace. Home, About us and Our future are separate HTML pages. No framework, package installation, API connection or secret is required.

## Preview locally

From this repository, run:

```sh
python3 -m http.server 8080 --directory site
```

Open http://localhost:8080. Stop the server with Ctrl+C.

## Check changes

```sh
python3 scripts/check_site.py
node --check site/assets/site.js
```

Also review desktop and mobile widths, navigation, category buttons and FAQ accordions. With JavaScript disabled, all pages and navigation remain available; the category explorer displays its default category with a text list of the other categories.

## First publication (human operator)

1. Review and push this repository's changes to `main`.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source. Do not select deployment from a branch.
3. In **Actions**, run **Check and publish website** from `main` if the first push ran before Pages was enabled.
4. Confirm the published site at https://admin-kbb.github.io/khetibadibazaar-website/.
5. Optionally restrict the `github-pages` environment to the `main` branch under **Settings → Environments**.

Future pushes to `main` validate and publish automatically. Pull requests run checks only. Manual runs publish only when run from `main`. The workflow follows GitHub's official [custom Pages workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) with deployment permissions confined to the publishing job.

Only `site/` is uploaded. Workflow files, this guide and validation scripts are excluded from the hosted artifact, though this public repository's source is visible on GitHub. Never copy app source, credentials, private screenshots or configuration into this repository.

## Custom domain (human operator)

The site works at the GitHub project URL and a custom domain without changing asset paths.

1. Verify ownership of the domain in your GitHub account's Pages settings before connecting it; see [domain verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages).
2. Set your chosen domain, such as `www.khetibadibazaar.com`, under this repository's **Settings → Pages → Custom domain**.
3. At the external DNS provider, set `www` to a CNAME targeting `admin-kbb.github.io` (no protocol or repository path). Replace conflicting records for `www` only if appropriate.
4. For the apex domain as well, follow GitHub's current [apex domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-an-apex-domain).
5. Preserve existing mail records and the `api` and `dev` delegations. No AWS changes are needed for the website.
6. Wait for DNS verification and certificate provisioning, enable **Enforce HTTPS**, then verify all three pages on your domain.

For an Actions publishing source, the custom domain is configured in repository settings; a CNAME file alone does not configure it. No domain has been hardcoded before your choice is confirmed.

## Editing content

- `site/index.html`: introduction, category explorer, app features and FAQs.
- `site/about.html`: purpose, audiences and principles.
- `site/future.html`: product direction and app availability.
- `site/assets/styles.css`: responsive layout, palette and typography.
- `site/assets/site.js`: mobile menu, category selection and copyright year.

The full content is in HTML and stays readable without JavaScript. Add official app store links to the availability section and appropriate calls to action only after actual store listings are published. Keep roadmap statements separate from released capabilities. Do not add invented testimonials, marketplace metrics, live prices or launch dates.

The site deliberately has no collection forms, tracking, cookies, local storage, payments or backend requests. Hosting providers may independently retain request logs. If data collection is added later, prepare the appropriate privacy information before enabling it.

## AI crawler preferences

`site/robots.txt` asks the listed AI training crawlers, AI search bots and AI retrieval agents not to crawl any website page or asset. Ordinary search engines and social link previews remain allowed. This is an opt-out for known agents, not a universal way to identify AI traffic. Review the list periodically as providers change their crawler names.

The workflow already publishes this file with the rest of `site/`. After you push and publication completes, confirm that **https://khetibadibazaar.com/robots.txt** returns HTTP 200 and the actual plain-text rules, rather than HTML or a 404. Requests to `www` should redirect to the configured primary domain. At the default GitHub project URL, the file is under `/khetibadibazaar-website/robots.txt`; crawlers look for `/robots.txt` at the host root, so the policy depends on the custom domain serving this site at its root.

`python3 scripts/check_site.py` checks that named AI agents are disallowed on pages and image assets, including versioned user-agent strings, while ordinary crawlers remain allowed. No network access is needed for these checks.

### Scope and limits

- Robots rules are voluntary and do not stop noncompliant scrapers, spoofed user agents, copying by visitors, or use of previously collected content. Some user-directed AI fetchers may ignore robots rules.
- This file applies only to this website's host. It does **not** protect the Flutter app, `api.khetibadibazaar.com`, `dev.khetibadibazaar.com`, or this public GitHub repository. Sensitive app/API content must be protected by server-side authentication and authorization; adding paths to robots.txt does not secure them.
- Allowing ordinary search indexing does not guarantee exclusion from every search engine's AI features or downstream reuse. We have not disabled normal search snippets or indexing.
- GitHub Pages serves static files. Stronger enforcement would need a proxy/CDN with bot controls and rate limits, alongside any application-level access controls. No DNS, hosting, API or cloud configuration has been changed here.
- No `llms.txt` is added: it is intended to help AI systems discover content, not to enforce an opt-out. Unrecognised meta tags and unsupported hosting configuration files are not treated as protection.

Provider references: [OpenAI](https://developers.openai.com/api/docs/bots), [Anthropic](https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), [Google](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers), [Apple](https://support.apple.com/en-au/119829), [Common Crawl](https://commoncrawl.org/ccbot), [Perplexity](https://docs.perplexity.ai/docs/resources/perplexity-crawlers), [Amazon](https://developer.amazon.com/docs/amazonbot/amazonbot.html), and [Meta](https://developers.facebook.com/docs/sharing/webmasters/web-crawlers).

## Branding and asset provenance

The logo is an unchanged copy of the current app's `frontend/assets/icons/app_icon.png`. The forest green (`#146c43`), harvest accent (`#c58b2a`), Poppins typography and warm surfaces follow the app's visual language.

The five category WebP files are the app's generated editorial category artwork. They illustrate categories and are not actual sale listings. Legacy seed photographs were not used because their original licensing metadata is incomplete. Poppins font files are bundled with their SIL Open Font License in `site/assets/fonts/OFL-Poppins.txt`. All site assets are local; no third-party font or image request is needed.
