<script lang="ts">
	import Legal from '#lib/legal/Legal.svelte';
	import { UPDATED, CO, EMAIL, ADDR, STATE } from '#lib/legal/facts.ts';
</script>

<Legal title="Terms of Service" description="The terms for using Scoo, including text message terms and referral credit.">
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
</Legal>
