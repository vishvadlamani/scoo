# Builds terms.html and privacy.html. DRAFT for legal review: bracketed items are facts only the
# owner can supply, and nothing here is legal advice.
mark = open('_mark.svg').read()
UPDATED = 'November 17, 2026'
CO = '[Company legal name]'
EMAIL = '[privacy@scoo.app]'
ADDR = '[Mailing address]'
STATE = '[State]'

TERMS = f'''
<h1>Terms of Service</h1>
<p class="meta">Last updated {UPDATED}</p>
<p>These terms are an agreement between you and {CO} ("Scoo", "we", "us"). They cover scoo.app and the texts and emails we send. By using Scoo, or by ticking the box to agree, you accept these terms and our <a href="/privacy">Privacy Policy</a>.</p>

<h2>1. What Scoo is</h2>
<p>Scoo helps people find local professionals ("pros"), such as plumbers, electricians, lawyers and insurance agents, and connects them by phone. Scoo is opening city by city. Until it opens in your area, signing up puts you on a waitlist: we save your request and tell you when Scoo is available near you.</p>
<p>Pros are independent businesses, not Scoo employees or agents. Scoo does not perform any service, and we do not guarantee any pro's work, prices, licensing, insurance or availability. Any agreement for work is between you and the pro.</p>
<p><b>Scoo is not for emergencies.</b> If anyone is in danger, there is a fire, or you smell gas, call 911 or your local emergency number.</p>

<h2>2. Who can use Scoo</h2>
<p>You must be at least 18 and in the United States. You agree to give accurate information, including a phone number or email address that is yours.</p>

<h2>3. Text messages and email</h2>
<p>When you give us your mobile number or email and agree to these terms, you agree that Scoo may send you texts and emails about your request, about Scoo opening near you, and about your account and referrals. These may include marketing messages. Texts may be sent using automated technology.</p>
<ul>
<li><b>Program:</b> Scoo notifications.</li>
<li><b>How often:</b> it varies, usually a few messages around your request and launch.</li>
<li><b>Cost:</b> Message and data rates may apply. Scoo does not charge for texts.</li>
<li><b>Opt out:</b> reply <b>STOP</b> to any text, or use the unsubscribe link in any email. We'll confirm and stop. You can rejoin by signing up again.</li>
<li><b>Help:</b> reply <b>HELP</b> to any text, or email {EMAIL}.</li>
<li>Agreeing to receive messages is not a condition of buying anything.</li>
<li>Mobile carriers are not liable for delayed or undelivered messages.</li>
</ul>
<p>If you give us a number that isn't yours, or your number changes, let us know so we stop messaging it.</p>

<h2>4. Referral credit</h2>
<p>You may get a personal invite link. Credit is earned as described on the sign-up page at the time (currently $10 when a friend you invite signs up, and $25 when a pro you invite joins and completes their first job through Scoo), up to $100 in total per person.</p>
<ul>
<li>Credit is Scoo platform credit only. It has no cash value, cannot be redeemed for cash, transferred or sold, and can be used only once Scoo opens in your area.</li>
<li>Invites must go to real people you know. Self-referrals, fake or duplicate accounts, paid ads using your link, and spam are not allowed. We may cancel credit earned that way.</li>
<li>We may change or end the referral program, or expire unused credit, with notice. Where the law prohibits it, the program is void.</li>
</ul>

<h2>5. For pros</h2>
<p>If you join as a pro, you confirm that you are authorised to act for the business, and that you hold the licences, permits and insurance your work requires.</p>
<p>Founding pros get Scoo's AI receptionist at no charge once Scoo opens in their area, subject to a fair-use limit we'll tell you before it switches on. New customer calls from Scoo are optional and paid per call: you'll see the price before you accept any, and you can set limits or pause at any time. Separate pro terms will apply once Scoo opens in your area.</p>

<h2>6. Using Scoo fairly</h2>
<p>Don't misuse Scoo. That includes submitting false requests, impersonating anyone, scraping or overloading the site, getting around our security checks, or using Scoo for anything unlawful or harassing.</p>

<h2>7. Our content</h2>
<p>Scoo's name, logo, illustrations and site are ours. You may not copy them except as needed to use Scoo. If you send us feedback, we may use it without owing you anything.</p>

<h2>8. Disclaimers</h2>
<p>Scoo is provided "as is" and "as available". To the fullest extent the law allows, we disclaim all warranties, express or implied, including fitness for a particular purpose. We don't promise when, or whether, Scoo will open in a given area, or that a pro will be available or respond within any time.</p>

<h2>9. Limits on liability</h2>
<p>To the fullest extent the law allows, Scoo is not liable for indirect, incidental, special or consequential damages, or for anything a pro does or fails to do. Our total liability for any claim relating to Scoo is limited to $100 or the amount you paid Scoo in the 12 months before the claim, whichever is greater. Some places don't allow these limits, so they may not apply to you.</p>

<h2>10. Changes and ending</h2>
<p>We may update these terms. If changes are significant, we'll tell you by text, email or on the site before they apply. You can stop using Scoo at any time, and we may suspend access for anyone who breaks these terms.</p>

<h2>11. Governing law</h2>
<p>These terms are governed by the laws of {STATE}, without regard to conflict-of-law rules. [Dispute resolution: to be decided with counsel, for example small claims or arbitration.]</p>

<h2>12. Contact</h2>
<p>{CO}<br>{ADDR}<br>{EMAIL}</p>

<h2>Credits</h2>
<p>ZIP code data © <a href="https://www.geonames.org/" rel="noopener">GeoNames</a>, used under <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener">CC BY 4.0</a>.</p>
'''

PRIVACY = f'''
<h1>Privacy Policy</h1>
<p class="meta">Last updated {UPDATED}</p>
<p>This policy explains what {CO} ("Scoo", "we") collects through scoo.app and our texts and emails, how we use it, and the choices you have.</p>

<h2>What we collect</h2>
<ul>
<li><b>What you tell us:</b> what you need help with, your answer to our follow-up question, your ZIP code, and your mobile number or email.</li>
<li><b>If you join as a pro:</b> your business name, trade, the ZIP you work in, mobile number and optional email.</li>
<li><b>Your consent:</b> the exact wording you agreed to and when, so we can show you opted in.</li>
<li><b>Referrals:</b> your invite code, and the code of whoever invited you.</li>
<li><b>Technical information:</b> your browser type, and your IP address, which we use to estimate your approximate city (to show a local message) and to block bots and abuse.</li>
</ul>
<p>We don't ask for your exact location, and we don't use advertising cookies on scoo.app.</p>

<h2>How we use it</h2>
<ul>
<li>To save your request and tell you when Scoo opens near you.</li>
<li>Once Scoo is live in your area, to connect you with a suitable pro and share your request with them.</li>
<li>To send the texts and emails you agreed to, and to honour opt-outs.</li>
<li>To decide where to launch next, using counts by area.</li>
<li>To run the referral program and prevent fraud and abuse.</li>
<li>To understand what you need. We may use automated tools, including AI services, to read the text of your request and sort it into a category. We send only the request text for this, never your phone number or email.</li>
</ul>

<h2>Who we share it with</h2>
<ul>
<li><b>Pros:</b> once Scoo is live in your area, the pro matched to your request receives your request and the contact details needed to reach you.</li>
<li><b>Service providers</b> that run Scoo for us, such as hosting and security (Cloudflare), our database, text and email delivery, and AI request sorting. They may use the information only to provide their service to us.</li>
<li><b>Legal reasons:</b> when the law requires it, or to protect people, Scoo or our users.</li>
<li><b>Business changes:</b> if Scoo is merged or sold, your information may transfer, still covered by this policy.</li>
</ul>
<p><b>We don't sell your personal information.</b> Mobile numbers and text-message opt-in consent are never shared with third parties or affiliates for their marketing.</p>

<h2>How long we keep it</h2>
<p>We keep your request and contact details until Scoo opens in your area and for a reasonable time afterwards, or until you ask us to delete them. Consent and opt-out records may be kept longer, as proof that we honoured your choices.</p>

<h2>Your choices</h2>
<ul>
<li>Reply <b>STOP</b> to any text, or use the unsubscribe link in any email.</li>
<li>Email {EMAIL} to see, correct or delete your information. We'll respond within the time the law requires.</li>
<li>Depending on your state, you may have more rights, such as knowing what we hold about you. We won't treat you differently for using them.</li>
</ul>

<h2>Security</h2>
<p>We use reasonable safeguards, including encryption in transit. No system is perfectly secure, so please contact us if you notice anything wrong.</p>

<h2>Children</h2>
<p>Scoo is for adults. We don't knowingly collect information from anyone under 18, and we'll delete it if we learn we have.</p>

<h2>Changes</h2>
<p>If we change this policy in a meaningful way, we'll update the date above and, where appropriate, tell you by text, email or on the site.</p>

<h2>Contact</h2>
<p>{CO}<br>{ADDR}<br>{EMAIL}</p>
'''

def page(title, body, desc):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Scoo</title><meta name="description" content="{desc}"><link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FFFFFF;--ink:#111111;--muted:#55595f;--accent:#FF6B4A;--line:#e7e5e0}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0E0E10;--ink:#EDEDED;--muted:#a7abb3;--accent:#FF7A5C;--line:#2a2a2e}}}}
:root[data-theme="dark"]{{--bg:#0E0E10;--ink:#EDEDED;--muted:#a7abb3;--accent:#FF7A5C;--line:#2a2a2e}}
*{{box-sizing:border-box}}html,body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Hanken Grotesk',system-ui,sans-serif}}
header{{display:flex;align-items:center;justify-content:space-between;padding:20px clamp(16px,4vw,48px);max-width:1100px;margin:0 auto}}
.logo{{display:inline-flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;font-size:26px;letter-spacing:-.02em}}
.logo .mark{{height:36px;width:auto;color:var(--ink)}}.logo .mouth{{stroke:var(--accent)}}
nav a{{color:var(--ink);margin-left:18px;font-size:15px}}
main{{max-width:720px;margin:0 auto;padding:8px 20px 72px;line-height:1.65;font-size:17px}}
h1{{font-weight:300;font-size:clamp(36px,5vw,52px);letter-spacing:-.03em;margin:16px 0 4px}}
h2{{font-weight:500;font-size:21px;margin:36px 0 8px}}
.meta{{color:var(--muted);margin:0 0 24px}}
.draft{{border:1.5px solid var(--accent);border-radius:14px;padding:12px 16px;font-size:15px;margin:0 0 8px}}
ul{{padding-left:20px}}li{{margin:6px 0}}a{{color:var(--ink)}}
footer{{max-width:720px;margin:0 auto;padding:24px 20px 48px;border-top:1.5px solid var(--line);color:var(--muted);font-size:14px}}footer a{{color:var(--muted);margin-right:16px}}
</style></head><body>
<header><a class="logo" href="/" aria-label="Scoo home">{mark}<span>scoo</span></a><nav><a href="/terms">Terms</a><a href="/privacy">Privacy</a></nav></header>
<main><p class="draft">Draft, pending legal review.</p>{body}</main>
<footer><a href="/">Home</a><a href="/pros">For pros</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a></footer>
</body></html>'''

open('terms.html', 'w').write(page('Terms of Service', TERMS, 'The terms for using Scoo, including text message terms and referral credit.'))
open('privacy.html', 'w').write(page('Privacy Policy', PRIVACY, 'What Scoo collects, how it is used and shared, and your choices.'))
print('ok')
