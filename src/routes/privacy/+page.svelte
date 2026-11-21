<script lang="ts">
	import Legal from '#lib/legal/Legal.svelte';
	import { UPDATED, CO, EMAIL, ADDR } from '#lib/legal/facts.ts';
</script>

<Legal title="Privacy Policy" description="What Scoo collects, how it is used and shared, and your choices.">
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
<li><b>The public, if you are a pro and ask for it:</b> a public profile shows your business name, trade, town, service area and the details you approve. It goes live only after we check it with you, and you can ask us to take it down at any time.</li>
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
</Legal>
