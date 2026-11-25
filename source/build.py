"""Builds the MyPowerfulNotes website into ../site (plain static files for Netlify).

    python3 build.py

Pages share one header and footer. Illustrations come from art.py; the logo from brand/.
"""
import os
import shutil
import subprocess

import art

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "..", "site")
BRAND = os.path.join(HERE, "..", "brand")
ROOT = os.path.join(HERE, "..")
SITE = "https://mypowerfulnotes.com"
UPDATED = "23 November 2026"
ISSUES = "https://github.com/joeljfraser-dotcom/notepen/issues"

NAV = [("/#features", "Features", "features"), ("/#screens", "Screens", "screens"), ("/privacy", "Privacy", "privacy"),
       ("/support", "Support", "support")]


def head(title, description, path):
    full = title if title == "MyPowerfulNotes" else f"{title} | MyPowerfulNotes"
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#1E242B">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MyPowerfulNotes">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/fonts/inter-regular.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="/fonts/interdisplay-semibold.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
'''


def header(current):
    links = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == current else ""}>{label}</a>' for href, label, key in NAV)
    return f'''<header class="site-head">
<div class="wrap">
<a class="brand" href="/" aria-label="MyPowerfulNotes home"><img src="/logo.svg" alt="" width="32" height="32"><span>My<b>Powerful</b>Notes</span></a>
<nav class="site-nav" aria-label="Main">{links}</nav>
</div>
</header>
'''


FOOTER = f'''<footer class="site-foot">
<div class="wrap">
<span>© 2026 MyPowerfulNotes</span>
<nav aria-label="Legal and help">
<a href="/privacy">Privacy policy</a>
<a href="/terms">Terms of use</a>
<a href="/support">Support</a>
<a href="/licences">Licences</a>
</nav>
</div>
</footer>
</body>
</html>
'''


def page(path, title, description, current, main):
    return head(title, description, path) + header(current) + f'<main id="main">\n{main}\n</main>\n' + FOOTER


# =================================================================================================================
# Home
# =================================================================================================================

def home():
    papers = ["Ruled", "Grid", "Dots", "Cornell", "Day planner", "Music", "Isometric", "Your own"]
    paper_items = "".join(f"<li>{art.paper(p)}{p}</li>" for p in papers)
    main = f'''
<section class="hero">
<div class="wrap">
<div class="hero-copy">
<h1>Handwritten notes on proper pages, on your PC and your tablet.</h1>
<p class="lead">Write with your pen on A4 paper, mark up PDFs, draw to scale and turn ticked boxes into a to-do list. Your notes are encrypted on your own devices, and nobody else can read them.</p>
<div class="buttons">
<a class="button primary" href="#features">See what it does</a>
<a class="button quiet" href="#privacy">How your notes stay private</a>
</div>
<p class="note">For Windows 11 and Android 11 or later. Free while it's being tested.</p>
</div>
<div class="hero-page">{art.hero_page()}</div>
</div>
</section>

<section class="section" id="features" aria-labelledby="features-title">
<div class="wrap">
<div class="section-head">
<h2 id="features-title">One page, everything on it</h2>
<p>Each page is a sheet of paper you write on with a pen. Everything else sits on the same page, so your notes stay together the way they would in a paper notebook.</p>
</div>
<div class="anatomy">
<ul class="callouts left">
<li class="a1"><h3>Ink that feels like a pen</h3><p>Pen, fineliner and highlighter with pressure, in your own colours. Low-latency ink on both Surface and S Pen.</p></li>
<li class="a3"><h3>Typed text and tables</h3><p>Headings, bullet lists and tables that wrap the same on every device.</p></li>
<li class="a5"><h3>Drawings to scale</h3><p>Lengths, angles, areas and sums. Change one length and the joined lines follow, keeping corners square.</p></li>
</ul>
<div class="sheet">{art.anatomy_page()}</div>
<ul class="callouts right">
<li class="a2"><h3>PDFs to write on</h3><p>Import a PDF or save a web page, then highlight, circle and write in the margins.</p></li>
<li class="a4"><h3>Ticks and flags become actions</h3><p>Draw a tick box or flag a line, and it lands in one Actions list with a due date and owner.</p></li>
<li class="a6"><h3>Links and sticky notes</h3><p>Add web links and keep them as resources for the page, section or notebook.</p></li>
</ul>
</div>

<div class="papers">
<div>
<h3>Paper for every job</h3>
<p>Choose ruled, grid, dot, Cornell, planner, music or isometric paper, or design your own. Pages come in A5 to A0, portrait or landscape, or as one continuous page that keeps going.</p>
</div>
<ul class="paper-list">{paper_items}</ul>
</div>

<ul class="more-list">
<li><h3>Search everything</h3><p>Typed text, handwriting and PDF text, across every notebook.</p></li>
<li><h3>A map of your notes</h3><p>See notebooks, pages and tags as a map, and add your own thoughts and links.</p></li>
<li><h3>Export when you need to</h3><p>Send a page or notebook as a PDF, with links that still work.</p></li>
<li><h3>Photos and pictures</h3><p>Take a photo with your tablet or phone, or add a picture, and write on and around it.</p></li>
<li><h3>Fill</h3><p>Tap inside a shape you've drawn to colour it in, under the ink.</p></li>
<li><h3>Talk to text</h3><p>Dictate into a text box using your device's own speech recognition.</p></li>
<li><h3>Sections and headers</h3><p>Split notebooks into sections and add a header and footer to every page.</p></li>
<li><h3>Daily snapshots</h3><p>A snapshot of your notes each day, and backup files that stay encrypted.</p></li>
</ul>
</div>
</section>

<section class="section tint" id="screens" aria-labelledby="screens-title">
<div class="wrap">
<div class="section-head">
<h2 id="screens-title">See it on your devices</h2>
<p>The same notebooks on your Windows PC, your Android tablet and your phone.</p>
</div>
<div class="screens">
<figure class="screen">{art.windows_notebook()}
<figcaption><h3>Writing on Windows</h3><p>Pick a pen, colour and width from the toolbar and write. The pages panel shows every page in the notebook, and the Resources list keeps the links that go with each one.</p></figcaption>
</figure>
<figure class="screen">{art.tablet_pdf()}
<figcaption><h3>Marking up a PDF on a tablet</h3><p>Open a contract or a set of plans, highlight what matters and write your questions beside it. The PDF itself is never changed, so you can always go back to the original.</p></figcaption>
</figure>
<figure class="screen">{art.cad_screen()}
<figcaption><h3>Drawing to scale</h3><p>Draw lines, rectangles and arcs at 1:50 or any scale. Tap a length to type a new one, or a sum such as B + 600. Angles, areas and perimeters update as you go.</p></figcaption>
</figure>
<div class="pair">
<figure class="screen">{art.map_screen()}
<figcaption><h3>The notes map</h3><p>Notebooks, pages, tags, your own thoughts and web links, joined up so you can see how a job fits together.</p></figcaption>
</figure>
<figure class="screen">{art.phone_actions()}
<figcaption><h3>Actions on your phone</h3><p>Every tick box and flag, with dates and the page it came from.</p></figcaption>
</figure>
</div>
</div>
<p class="disclaimer">These are illustrations of the app's screens.</p>
</div>
</section>

<section class="section" id="privacy" aria-labelledby="privacy-title">
<div class="wrap">
<div class="private">
<div class="section-head">
<h2 id="privacy-title">Private by design</h2>
<p>MyPowerfulNotes has no server and no account with us. Your notes are encrypted on your device before they're saved, and they sync through your own cloud storage as encrypted files.</p>
<p><a href="/privacy">Read the privacy policy</a></p>
</div>
<div>{art.sync_diagram()}</div>
</div>
<dl class="facts">
<div><dt>Encrypted on your device</dt><dd>Every page, PDF and setting is stored with AES-256-GCM encryption, using a key that stays on your device.</dd></div>
<div><dt>Only you hold the recovery code</dt><dd>Your recovery code opens your notes on a new device. Nobody else has it, so nobody else can open them.</dd></div>
<div><dt>Your cloud, your files</dt><dd>Sync uses your own OneDrive or Google Drive, which only ever sees encrypted files.</dd></div>
<div><dt>No tracking</dt><dd>No ads, no analytics and no crash reports sent anywhere.</dd></div>
<div><dt>Nothing leaves unless you choose</dt><dd>Sync, opening web pages and sharing a file only happen when you start them.</dd></div>
<div><dt>Backups stay encrypted</dt><dd>Backup files are as protected as your notes. Export a PDF when you want a copy anyone can read.</dd></div>
</dl>
</div>
</section>

<section class="section tint" id="platforms" aria-labelledby="platforms-title">
<div class="wrap">
<div class="section-head">
<h2 id="platforms-title">Windows and Android, the same notebooks</h2>
<p>Both apps read and write the same encrypted files, so you can start a page on your PC and finish it on your tablet.</p>
</div>
<div class="platforms">
<div class="platform">
<h3>Windows</h3>
<p>For Windows 11 PCs and tablets with a pen, such as Surface.</p>
<ul>
<li>Pen, mouse, touch and keyboard</li>
<li>Reads your handwriting so you can search it</li>
<li>Shows a code to link your tablet or phone</li>
</ul>
</div>
<div class="platform">
<h3>Android</h3>
<p>For tablets and phones running Android 11 or later, including S Pen devices.</p>
<ul>
<li>Tablet and phone layouts</li>
<li>Unlock with your fingerprint, face or PIN</li>
<li>Scan the code on your PC to set up in a minute</li>
</ul>
</div>
</div>
<div class="status">
<p><strong>Being tested now</strong>MyPowerfulNotes is in testing and free to use. It's planned for the Microsoft Store and Google Play.</p>
<a class="button" href="/support">Get help or send feedback</a>
</div>
</div>
</section>
'''
    return page("/", "MyPowerfulNotes",
                "Handwritten notes on A4 pages for Windows and Android. Write with a pen, mark up PDFs, draw to scale and keep everything encrypted on your own devices.",
                "home", main)


# =================================================================================================================
# Documents
# =================================================================================================================

def doc(path, title, description, current, intro, sections, show_updated=True):
    toc = "".join(f'<li><a href="#{sid}">{heading}</a></li>' for sid, heading, _ in sections)
    body = "".join(f'<h2 id="{sid}">{heading}</h2>\n{html}\n' for sid, heading, html in sections)
    updated = f'<p class="updated">Last updated {UPDATED}</p>' if show_updated else ""
    main = f'''<div class="doc">
<div class="wrap">
<header><h1>{title}</h1><p>{intro}</p>{updated}</header>
<nav class="toc" aria-label="On this page"><p>On this page</p><ol>{toc}</ol></nav>
<article class="prose">
{body}
</article>
</div>
</div>'''
    return page(path, title, description, current, main)


def privacy():
    s = [
        ("summary", "In short", f'''<div class="callout">
<p>MyPowerfulNotes keeps your notes on your own devices, encrypted. We don't run a server, you don't make an account with us, and the app has no advertising, analytics or crash reporting of its own. We can't see your notes, and we don't collect information about you. On Android, two Google components the app uses (handwriting reading and the link code scanner) send Google basic diagnostic information about the device and app; never your notes (see <a href="#services">When the app uses other services</a>).</p>
</div>
<p>This policy explains what the app does with your information, including the few times it connects to other services, and only when you ask it to.</p>'''),
        ("who", "Who we are", f'''<p>MyPowerfulNotes ("the app", "we", "us") is an independent app for Windows and Android, developed in Australia. This policy covers the apps and this website.</p>
<p>To contact us about privacy, <a href="{ISSUES}">open an issue on GitHub</a>. Issues are public, so don't include personal details or anything from your notes; say you'd like to talk privately and we'll arrange a private way to reply.</p>'''),
        ("notes", "Your notes stay on your device", '''<p>Your notebooks, pages, handwriting, typed text, drawings, imported PDFs, saved web pages and settings are stored on your device, encrypted with AES-256-GCM. The key is protected by your device: Windows Data Protection on a PC, and the Android Keystore (with your fingerprint, face or PIN) on Android.</p>
<p>When you start, the app gives you a recovery code. It's the only other way to open your notes, for example on a new device. Only you hold it: it's never sent to us, and we can't reset it or recover your notes without it.</p>
<p>The app doesn't send your notes, or anything about how you use it, to us or anyone else.</p>'''),
        ("sync", "Sync with your own OneDrive or Google Drive (optional)", f'''<p>If you turn on sync, you sign in to your own Microsoft or Google account and the app keeps copies of its files there. Files are encrypted on your device before they're uploaded, so Microsoft and Google store only data they can't read. We never receive your files. The sign-in is kept only on your device.</p>
<ul>
<li><strong>OneDrive:</strong> the app can only use its own folder under Apps in your OneDrive (permission <code>Files.ReadWrite.AppFolder</code>), plus <code>openid</code>, <code>profile</code> and <code>offline_access</code> to stay signed in and show which account is connected. It can't see your other files.</li>
<li><strong>Google Drive:</strong> the app asks to see, create and delete its own configuration data in your Google Drive (<code>drive.appdata</code>): a hidden folder only this app can use. It also asks for your email address and basic sign-in (<code>openid</code>, <code>email</code>) to show which account is connected. It can't see or change any other file in your Drive.</li>
</ul>
<p>Information received from Google APIs is used only to provide sync to you. It isn't sold, shared, used for advertising or read by people. MyPowerfulNotes' use and transfer of information received from Google APIs adheres to the <a href="https://developers.google.com/terms/api-services-user-data-policy">Google API Services User Data Policy</a>, including the Limited Use requirements.</p>
<p>Microsoft and Google handle your account and storage under their own privacy policies, and may store data outside Australia. Because the files are encrypted before upload, your notes stay unreadable wherever they're stored.</p>
<p>Linking a phone or tablet by scanning a code on your PC shares the sync details between your own devices. The code is shown on your screen and isn't sent anywhere.</p>'''),
        ("services", "When the app uses other services", '''<p>A few features rely on your device or on other companies. Each one only runs when you use it.</p>
<table>
<thead><tr><th>Feature</th><th>What happens</th></tr></thead>
<tbody>
<tr><td>Reading handwriting</td><td>On Windows, the app uses Windows' own handwriting recognition on your PC. On Android, it uses Google ML Kit on your device: the first time you turn it on, a language model is downloaded from Google. Your ink is read on the device and isn't sent anywhere. Reading is off until you turn it on. While it's on, ML Kit sends Google diagnostic and usage information about the device and the app (such as the device model, Android version, the app's name and version, and how well the feature performed), encrypted in transit. It doesn't include your ink or notes, and Google says it doesn't share it with third parties.</td></tr>
<tr><td>Talk to text</td><td>Uses your device's speech recognition (Windows voice typing, or Android's speech service). The app only receives the words. Microsoft or Google may process your voice under their own policies; on Android the app asks for on-device recognition first.</td></tr>
<tr><td>Web pages and links</td><td>When you add a web page or open a link, the app loads that site as a browser would, and the site sees your connection as it would in a browser. It may set cookies in the app's web view, which you can clear on Windows.</td></tr>
<tr><td>Photos and pictures</td><td>A photo you take or a picture you add is kept inside your notes, encrypted, like everything else. Before it's kept it is saved again, which leaves out the camera's details (such as where and when it was taken). On Android the photo is taken by your camera app, so MyPowerfulNotes doesn't need camera permission, and it only passes through the app's private storage on the way. On Windows the app uses the camera only while the Take a photo window is open, with your permission.</td></tr>
<tr><td>Scanning a link code (Android)</td><td>Uses Google's code scanner in Google Play services. The app doesn't need camera permission and receives only the code. Google Play services may send Google similar diagnostic information about the scanner; it never sees your notes.</td></tr>
<tr><td>Sharing and exporting</td><td>When you export a PDF or share a file, a readable copy goes where you choose to send it. Temporary copies made for sharing are kept in the app's private storage and cleared.</td></tr>
</tbody>
</table>
<p>The app doesn't include AI features that send your content to an AI service. If we add any, they'll only run when you start them on a page or notebook, and this policy will say which service receives what before they're released.</p>'''),
        ("permissions", "Permissions", '''<ul>
<li><strong>Android:</strong> internet access (for sync, web pages and the handwriting model) and biometric access (to unlock with your fingerprint, face or PIN). The app doesn't ask for your contacts, location, camera or microphone: photos are taken by your camera app, and pictures are chosen with Android's own picker.</li>
<li><strong>Windows:</strong> the app runs in its own package and stores its files in its own app data folder. It asks to use the camera only when you choose to take a photo.</li>
</ul>'''),
        ("logs", "Problem logs", '''<p>If the app closes unexpectedly, it writes a short problem log on your device, with the app version, the device type and where the error happened. It never contains your notes. It stays on your device unless you choose to share it with us.</p>'''),
        ("website", "This website", '''<p>This website has no cookies, analytics or tracking. It's hosted by Netlify, which keeps standard server logs (such as IP addresses and the pages requested) to run and secure the service, under <a href="https://www.netlify.com/privacy/">Netlify's privacy policy</a>.</p>'''),
        ("delete", "Removing your data", '''<ul>
<li><strong>On a device:</strong> delete notebooks in the app, or uninstall it. Uninstalling removes the app's files from that device.</li>
<li><strong>Google Drive:</strong> in Google Drive, open Settings, then Manage apps, find MyPowerfulNotes (or NotePen, its earlier name) and choose Delete hidden app data. To remove its access, visit <a href="https://myaccount.google.com/permissions">your Google Account's third-party access page</a>.</li>
<li><strong>OneDrive:</strong> delete the app's folder under Apps in your OneDrive, and remove its access at <a href="https://account.live.com/consent/Manage">account.live.com/consent/Manage</a>.</li>
<li><strong>Backup files</strong> you've saved yourself stay where you put them until you delete them.</li>
</ul>
<p>There's no account with us to delete, because we don't hold any of your data.</p>'''),
        ("children", "Children", '''<p>The app isn't designed for children under 13, and we don't knowingly collect information from anyone, including children.</p>'''),
        ("rights", "Your privacy rights", f'''<p>Because we don't collect or hold personal information about you, there's normally nothing for us to give you access to or correct. If you have a question or a complaint about privacy, <a href="{ISSUES}">contact us</a> and we'll reply within 30 days. If you're not satisfied with our reply, you can contact the <a href="https://www.oaic.gov.au/">Office of the Australian Information Commissioner</a>.</p>'''),
        ("changes", "Changes to this policy", '''<p>If the way the app handles information changes, we'll update this policy and the date at the top before the change is released. For significant changes, the app will also tell you.</p>'''),
    ]
    return doc("/privacy", "Privacy policy",
               "How MyPowerfulNotes handles your information: notes encrypted on your device, optional sync through your own cloud, and no tracking.",
               "privacy", "How MyPowerfulNotes handles your information. The short version: your notes are encrypted on your devices, and we never see them.", s)


def terms():
    s = [
        ("about", "About these terms", f'''<p>These terms apply when you download or use MyPowerfulNotes ("the app") on Windows or Android, and this website. By using the app you agree to them. If you don't agree, please don't use the app.</p>
<p>The app is published by the developer of MyPowerfulNotes ("we", "us"). You can contact us by <a href="{ISSUES}">opening an issue on GitHub</a>.</p>'''),
        ("licence", "Your licence to use the app", '''<p>We give you a personal, non-exclusive, non-transferable licence to install and use the app on devices you own or control, for your own personal or work use, under these terms. We keep all rights in the app itself, including its code, design and name.</p>
<p>You may not sell, rent or redistribute the app, or copy, change or reverse engineer it, except where the law allows you to.</p>'''),
        ("price", "Price and future purchases", '''<p>The app is free while it's being tested. In future we may charge for it, for example as a one-off purchase or as paid upgrades for new major versions. If we do:</p>
<ul>
<li>the price will be shown in the Microsoft Store or Google Play before you buy, and payment will be handled by the store under its own terms;</li>
<li>refunds will follow the store's refund policy, as well as your rights under the Australian Consumer Law;</li>
<li>anything you already have will keep working, and you'll always be able to open, export and back up your existing notes.</li>
</ul>'''),
        ("testing", "Test versions", '''<p>Test versions are early releases and may have bugs, change between versions, or lose features. Keep backups while you use them (see below).</p>'''),
        ("your-notes", "Your notes, and keeping them safe", '''<p>Your notes belong to you. We don't own them, see them or keep copies of them.</p>
<p>Because your notes are encrypted on your device and we hold no copy of your key, <strong>you are responsible for keeping your recovery code safe and keeping backups</strong>. If you lose your recovery code and can't unlock your notes on any of your devices, nobody can recover them, including us. We recommend you:</p>
<ul>
<li>store your recovery code somewhere safe, away from your devices;</li>
<li>turn on daily backups to a folder of your choice, or save backup files regularly;</li>
<li>export important pages to PDF if you need a copy outside the app.</li>
</ul>'''),
        ("drawings", "Drawings, measurements and actions", '''<p>The drawing tool's lengths, angles, areas, perimeters and sums, and the dates and reminders in the Actions list, are aids to help you work. They depend on what you enter and on the accuracy of your drawing, and they may contain errors.</p>
<p><strong>Check measurements and calculations independently before you rely on them</strong> for building, manufacturing, ordering materials, quoting, safety or legal purposes. Handwriting recognition and search may also miss or misread words.</p>'''),
        ("third-parties", "Other services", '''<p>Sync uses your own Microsoft OneDrive or Google Drive account, web pages come from their own sites, and some features use services from Microsoft or Google. Those services are provided by their owners under their own terms, and we're not responsible for their availability, changes or content. Storage limits and any charges for them are between you and that provider.</p>'''),
        ("use", "Using the app responsibly", '''<ul>
<li>Use the app lawfully, and only import content you have the right to use.</li>
<li>If you keep work notes in the app, check that your employer allows it, including storing them in your personal cloud storage.</li>
<li>Don't try to interfere with the services the app connects to.</li>
</ul>'''),
        ("acl", "Your rights under the Australian Consumer Law", '''<p>Nothing in these terms excludes, restricts or changes any right or remedy, or any guarantee, warranty or other term implied or imposed by the <em>Competition and Consumer Act 2010</em> (Cth), including the Australian Consumer Law, or any other law, that can't lawfully be excluded or limited ("non-excludable rights").</p>
<p>If you're a consumer, our goods and services come with guarantees that cannot be excluded under the Australian Consumer Law. Where we're allowed to limit our liability for failing to meet a non-excludable right, our liability is limited, at our option, to supplying the app or services again, or paying the cost of having them supplied again.</p>'''),
        ("disclaimer", "No other warranties", '''<p>Apart from your non-excludable rights, the app and this website are provided "as is" and "as available". To the extent the law allows, we don't promise that the app will be free of errors or interruptions, that it will work with every device, or that it will meet your particular needs, and we exclude all other warranties, express or implied.</p>'''),
        ("liability", "Limits on our liability and release for loss", '''<p>To the extent the law allows, and apart from your non-excludable rights:</p>
<ol>
<li>we are not liable for any loss of or damage to your notes, files or other data, however it happens, including through lost recovery codes or devices, device failure, uninstalling the app, sync conflicts, or problems with OneDrive, Google Drive or other services;</li>
<li>we are not liable for any indirect or consequential loss, or for loss of profit, revenue, business, opportunity, goodwill or time, arising from or in connection with the app, this website or these terms;</li>
<li>we are not liable for loss arising from relying on measurements, calculations, recognised handwriting, search results or reminders in the app without checking them;</li>
<li>while the app is free, our total liability to you for all claims is limited to AU$100; and if you've paid for the app, it's limited to the amount you paid for it in the 12 months before the claim.</li>
</ol>
<p>By using the app, you agree to release us from claims for the losses above, to the extent the law allows. This doesn't limit liability for anything that can't be limited by law, such as liability for fraud.</p>'''),
        ("indemnity", "Your indemnity", '''<p>To the extent the law allows, you agree to indemnify us against any claim, loss or cost (including reasonable legal costs) arising from content you put in the app or share from it, your breach of these terms, or your breach of anyone else's rights. This doesn't apply to the extent the loss was caused by us.</p>'''),
        ("changes", "Changes and ending", '''<p>We may update the app, add or remove features, or stop offering it. We may also update these terms; we'll post the new version here with a new date, and for significant changes the app will tell you. If you keep using the app after a change, the new terms apply.</p>
<p>You can stop using the app at any time by uninstalling it. Before you do, make sure you have a backup or PDF export of anything you want to keep.</p>'''),
        ("law", "Governing law", '''<p>These terms are governed by the laws of New South Wales, Australia. You and we submit to the non-exclusive jurisdiction of its courts and the courts that can hear appeals from them. If any part of these terms can't be enforced, the rest still applies.</p>'''),
    ]
    return doc("/terms", "Terms of use",
               "The terms for using MyPowerfulNotes, including your rights under the Australian Consumer Law, keeping backups, and limits on liability.",
               "terms", "The agreement between you and us when you use MyPowerfulNotes. Please read the parts about keeping your recovery code and backups safe.", s)


def support():
    faq = [
        ("I've lost my recovery code", '''<p>If you can still open your notes on your PC, make a new one: open More, then App lock, and choose New recovery code. The old code stops working, so store the new one somewhere safe, away from your devices. If you can't unlock your notes on any device and don't have the code, they can't be recovered: the code is the only key, and nobody else holds it.</p>'''),
        ("How do I move my notes to a new device?", '''<p>Turn on sync on your current device (More, then Sync), then install the app on the new one and choose Set up from OneDrive or Set up from Google Drive. On a PC you can choose Link a phone or tablet and scan the code with the new device instead of typing your recovery code. You can also open a backup file on the new device and unlock it with your recovery code.</p>'''),
        ("How do backups work?", '''<p>The app takes a snapshot of your notes once a day and keeps the last 14. You can also save backup files, or have one saved every day to a folder you choose (the newest 3 are kept). Backup files stay encrypted and open with your recovery code.</p>'''),
        ("Can I use the app without sync?", '''<p>Yes. Sync is optional, and everything works offline. Without sync, keep regular backup files, because your notes are only on that device.</p>'''),
        ("Why does a page say it was saved by a newer version?", '''<p>Another of your devices has a newer version of the app that saved something this one doesn't understand yet. Update the app on this device. Until then, it won't change those notes, so nothing is lost.</p>'''),
        ("The app closed unexpectedly", f'''<p>The app keeps a short problem log on your device, which never contains your notes. On Android it offers to share the log when it next starts. Attach it to an <a href="{ISSUES}">issue on GitHub</a> with a description of what you were doing.</p>'''),
        ("Which devices does it work on?", '''<p>Windows 11 PCs and tablets (a pen is recommended), and Android 11 or later on tablets and phones, including Samsung S Pen devices.</p>'''),
        ("NotePen? Is that the same app?", '''<p>Yes. MyPowerfulNotes was called NotePen while it was first being built. Existing notes, sync and backups carry on as they were.</p>'''),
    ]
    faq_html = "".join(f"<details><summary>{q}</summary>{a}</details>" for q, a in faq)
    s = [
        ("contact", "Get help or send feedback", f'''<p>To report a problem, ask a question or suggest a feature, <a href="{ISSUES}">open an issue on GitHub</a>. Say which device you're using and what you were doing when the problem happened.</p>
<div class="callout"><p>Issues are public. Never post your recovery code, and don't include anything from your notes or personal details. If you need to talk privately, say so in the issue and we'll arrange a private way to reply.</p></div>'''),
        ("faq", "Common questions", faq_html),
        ("delete", "Removing your data", '''<p>MyPowerfulNotes doesn't have accounts, so there's nothing to delete with us. To remove your notes:</p>
<ul>
<li><strong>From a device:</strong> uninstall the app (or delete notebooks in it).</li>
<li><strong>From Google Drive:</strong> in Google Drive, open Settings, then Manage apps, find MyPowerfulNotes (or NotePen) and choose Delete hidden app data. Remove its access at <a href="https://myaccount.google.com/permissions">myaccount.google.com/permissions</a>.</li>
<li><strong>From OneDrive:</strong> delete the app's folder under Apps, and remove its access at <a href="https://account.live.com/consent/Manage">account.live.com/consent/Manage</a>.</li>
<li><strong>Backup files</strong> are wherever you saved them; delete them there.</li>
</ul>'''),
        ("documents", "Policies", '''<ul>
<li><a href="/privacy">Privacy policy</a></li>
<li><a href="/terms">Terms of use</a></li>
<li><a href="/licences">Open-source licences</a></li>
</ul>'''),
    ]
    return doc("/support", "Support",
               "Help with MyPowerfulNotes: recovery codes, moving to a new device, backups, removing your data and how to get in touch.",
               "support", "Answers to common questions, how to remove your data, and how to get in touch.", s, show_updated=False)


def licences():
    ofl = open(os.path.join(HERE, "static", "fonts", "OFL.txt")).read().replace("&", "&amp;").replace("<", "&lt;")
    s = [
        ("apps", "In the apps", '''<p>MyPowerfulNotes is built with these components, used under their licences:</p>
<table>
<thead><tr><th>Component</th><th>Used for</th><th>Licence</th></tr></thead>
<tbody>
<tr><td>Inter typeface (Rasmus Andersson)</td><td>Text on Android and this website</td><td>SIL Open Font License 1.1 (below)</td></tr>
<tr><td>AndroidX Ink, Input Motion Prediction and Core</td><td>Pen ink on Android</td><td><a href="https://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a></td></tr>
<tr><td>Kotlin standard library</td><td>Android app</td><td><a href="https://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a></td></tr>
<tr><td>Google ML Kit Digital Ink Recognition</td><td>Reading handwriting on Android</td><td><a href="https://developers.google.com/ml-kit/terms">ML Kit Terms of Service</a></td></tr>
<tr><td>Google Play services (sign-in, code scanner)</td><td>Google Drive sign-in and link codes on Android</td><td><a href="https://developers.google.com/terms">Google APIs Terms of Service</a></td></tr>
<tr><td>Windows App SDK and WinUI 3</td><td>Windows app</td><td><a href="https://github.com/microsoft/WindowsAppSDK">Microsoft licence terms</a></td></tr>
<tr><td>.NET</td><td>Windows app</td><td><a href="https://github.com/dotnet/runtime/blob/main/LICENSE.TXT">MIT License</a></td></tr>
</tbody>
</table>
<p>Microsoft, Windows, OneDrive and Surface are trademarks of the Microsoft group of companies. Google, Android, Google Drive and Google Play are trademarks of Google LLC. MyPowerfulNotes isn't affiliated with or endorsed by Microsoft or Google.</p>'''),
        ("inter", "Inter: SIL Open Font License 1.1", f'<pre class="licence">{ofl}</pre>'),
    ]
    return doc("/licences", "Open-source licences",
               "The open-source components and licences used in MyPowerfulNotes.",
               "", "The open-source software and fonts that MyPowerfulNotes is built with.", s, show_updated=False)


def not_found():
    main = '''<section class="not-found"><div class="wrap">
<h1>This page isn't here</h1>
<p>The link may be old, or the address mistyped. Try the <a href="/">home page</a>, <a href="/support">support</a> or the <a href="/privacy">privacy policy</a>.</p>
</div></section>'''
    return page("/404", "Page not found", "This page isn't here.", "", main)


# =================================================================================================================
# Assets
# =================================================================================================================

def run(cmd):
    subprocess.run(cmd, check=True)


def fonts(out):
    from fontTools.subset import Options, Subsetter, parse_unicodes
    from fontTools.ttLib import TTFont
    unicodes = parse_unicodes("U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-203A,U+2044,U+20AC,U+2122,U+2190-2193,U+2212")
    src = "/usr/share/fonts/opentype/inter/"
    for name, file in (("inter-regular", "Inter-Regular.otf"), ("inter-semibold", "Inter-SemiBold.otf"),
                       ("interdisplay-semibold", "InterDisplay-SemiBold.otf")):
        opts = Options()
        opts.layout_features = ["kern", "liga", "calt", "cv11", "ss01", "tnum"]
        opts.flavor = "woff"
        font = TTFont(src + file)
        sub = Subsetter(opts)
        sub.populate(unicodes=unicodes)
        sub.subset(font)
        font.flavor = "woff"
        font.save(os.path.join(out, name + ".woff"))


def icons(out):
    brand = BRAND
    shutil.copy(os.path.join(brand, "mark.svg"), os.path.join(out, "logo.svg"))
    shutil.copy(os.path.join(brand, "mark-small.svg"), os.path.join(out, "favicon.svg"))
    tmp = "/tmp/mpn-icons"
    os.makedirs(tmp, exist_ok=True)
    for s in (16, 32, 48):
        run(["rsvg-convert", "-w", str(s), os.path.join(brand, "mark-small.svg"), "-o", f"{tmp}/f{s}.png"])
    run(["convert", f"{tmp}/f16.png", f"{tmp}/f32.png", f"{tmp}/f48.png", os.path.join(out, "favicon.ico")])
    # Square, full-bleed versions for phones (they round the corners themselves).
    square = open(os.path.join(brand, "mark.svg")).read().replace('rx="116"', 'rx="0"')
    open(f"{tmp}/square.svg", "w").write(square)
    run(["rsvg-convert", "-w", "180", f"{tmp}/square.svg", "-o", os.path.join(out, "apple-touch-icon.png")])
    run(["rsvg-convert", "-w", "192", os.path.join(brand, "mark.svg"), "-o", os.path.join(out, "icon-192.png")])
    run(["rsvg-convert", "-w", "512", os.path.join(brand, "mark.svg"), "-o", os.path.join(out, "icon-512.png")])


def og_image(out):
    page = art.hero_page().replace('<svg viewBox="-6 -6 432 608"', '<svg x="700" y="70" width="430" height="622" viewBox="-6 -6 432 608"')
    page = page.replace('class="writing', 'class="done')
    logo = open(os.path.join(BRAND, "mark.svg")).read().replace("<svg ", '<svg x="80" y="86" width="64" height="64" ', 1)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<defs><pattern id="d" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.1" fill="#D6D8D4"/></pattern></defs>
<rect width="1200" height="630" fill="#F3F3F0"/><rect width="1200" height="630" fill="url(#d)"/>
{logo}
<text x="160" y="129" font-family="Inter" font-weight="600" font-size="30" fill="#1E242B">My<tspan fill="#0E6E66">Powerful</tspan>Notes</text>
<text font-family="Inter Display" font-weight="600" font-size="58" fill="#1E242B" letter-spacing="-1.2">
<tspan x="80" y="262">Handwritten notes on</tspan><tspan x="80" y="330">proper pages, on your</tspan><tspan x="80" y="398">PC and your tablet.</tspan></text>
<text x="80" y="470" font-family="Inter" font-size="24" fill="#4A535C">Windows and Android. Encrypted on your devices.</text>
<g transform="rotate(-2.5 915 380)">{page}</g>
</svg>'''
    open("/tmp/mpn-og.svg", "w").write(svg)
    run(["rsvg-convert", "-w", "1200", "-h", "630", "/tmp/mpn-og.svg", "-o", os.path.join(out, "og-image.png")])


NETLIFY_TOML = """# Netlify publishes site/ as it is (no build step). Headers and redirects are in site/_headers and
# site/_redirects, so they also apply if the folder is dragged into Netlify by hand.
[build]
  publish = "site"
  command = ""
"""

HEADERS = """/*
  Content-Security-Policy: default-src 'none'; img-src 'self' data:; style-src 'self'; font-src 'self'; manifest-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Cross-Origin-Opener-Policy: same-origin

/fonts/*
  Cache-Control: public, max-age=31536000, immutable
"""

REDIRECTS = """https://www.mypowerfulnotes.com/*  https://mypowerfulnotes.com/:splat  301!
/privacy-policy  /privacy  301
/terms-of-use  /terms  301
"""


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "fonts"))
    pages = {"index.html": home(), "privacy.html": privacy(), "terms.html": terms(), "support.html": support(),
             "licences.html": licences(), "404.html": not_found()}
    for name, html in pages.items():
        open(os.path.join(DIST, name), "w").write(html)
    shutil.copy(os.path.join(HERE, "static", "style.css"), DIST)
    shutil.copy(os.path.join(HERE, "static", "fonts", "OFL.txt"), os.path.join(DIST, "fonts"))
    fonts(os.path.join(DIST, "fonts"))
    icons(DIST)
    og_image(DIST)
    open(os.path.join(ROOT, "netlify.toml"), "w").write(NETLIFY_TOML)
    open(os.path.join(DIST, "_headers"), "w").write(HEADERS)
    open(os.path.join(DIST, "_redirects"), "w").write(REDIRECTS)
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = ["/", "/privacy", "/terms", "/support", "/licences"]
    open(os.path.join(DIST, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(DIST, "site.webmanifest"), "w").write(
        '{"name":"MyPowerfulNotes","short_name":"MyPowerfulNotes","icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png"},'
        '{"src":"/icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#0E6E66","background_color":"#F2F4F3","display":"browser"}\n')
    print("built", sorted(os.listdir(DIST)))


if __name__ == "__main__":
    main()
