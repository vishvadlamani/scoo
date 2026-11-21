<!-- On the list: the visitor's place in line, how close their area is to opening, and two invite
     links, one for friends and one for pros, each with its own share buttons. -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { ART_DONE } from './art.ts';
	import type { Joined } from './flow.ts';

	let { joined }: { joined: Joined } = $props();

	type Tab = 'f' | 'p';
	let tab = $state<Tab>('f');
	let copied = $state<Record<Tab, boolean>>({ f: false, p: false });
	let meter = $state(0);

	const links: Record<Tab, string> = $derived({ f: 'scoo.app/r/' + joined.code, p: 'scoo.app/pro/' + joined.code });
	const msgF = $derived(
		`I just joined Scoo, get a pro to call you back in 60 seconds. Join with my link and we both get $10: https://${links.f}`
	);
	const msgP = $derived(
		`Thought of you: Scoo gives pros a free AI receptionist that answers the calls you miss and books the job. Claim yours: https://${links.p}`
	);

	onMount(() => {
		// Two frames, so the bar has been laid out at zero and the width transition runs.
		requestAnimationFrame(() =>
			requestAnimationFrame(
				() => (meter = Math.max(3, Math.min(100, Math.round((joined.waiting / joined.goal) * 100))))
			)
		);
	});

	const copy = (t: Tab) => {
		navigator.clipboard?.writeText('https://' + links[t]);
		copied[t] = true;
	};
	const whatsapp = (msg: string) => open('https://wa.me/?text=' + encodeURIComponent(msg));
	const text = (msg: string) => (location.href = 'sms:?&body=' + encodeURIComponent(msg));
	const email = (msg: string) => (location.href = 'mailto:?subject=Scoo&body=' + encodeURIComponent(msg));
	const facebook = (url: string) =>
		open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent('https://' + url));
	const more = (msg: string) =>
		navigator.share ? navigator.share({ text: msg }).catch(() => {}) : navigator.clipboard.writeText(msg);
</script>

<div class="art" id="done-art">{@html ART_DONE}</div>
<h1 id="done-title">You're on the list!</h1>
<p class="lead" id="done-lead">
	You're #{joined.position.toLocaleString()} in {joined.areaLabel || 'your area'}. We'll {joined.via === 'email'
		? 'email'
		: 'text'} you the moment Scoo opens in {joined.town || 'your area'}.
</p>
<a class="primary letmein" href="/app" id="letmein"
	>Let me in <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" /></svg></a
>
<div class="meter" aria-label="Progress to launch"><i style:width="{meter}%"></i></div>
<div class="tabs" role="tablist">
	<button role="tab" aria-selected={tab === 'f'} onclick={() => (tab = 'f')}>Know a friend?</button><button
		role="tab"
		aria-selected={tab === 'p'}
		onclick={() => (tab = 'p')}>Know a pro?</button
	>
</div>
<div class="tab" data-p="f" hidden={tab !== 'f'}>
	<p>
		You each get <b>$10 Scoo credit</b> when they join, and <span class="cityname">{joined.town || joined.city}</span> opens
		sooner.
	</p>
	<div class="link">
		<span id="flink">{links.f}</span><button type="button" class="cp" onclick={() => copy('f')}
			>{copied.f ? 'Copied' : 'Copy'}</button
		>
	</div>
	<div class="share">
		<button type="button" onclick={() => whatsapp(msgF)}>WhatsApp</button><button type="button" onclick={() => text(msgF)}
			>Text</button
		><button type="button" onclick={() => facebook(links.f)}>Facebook</button><button
			type="button"
			onclick={() => email(msgF)}>Email</button
		>
	</div>
</div>
<div class="tab" data-p="p" hidden={tab !== 'p'}>
	<p>
		Know a great pro? Send them your link: they get Scoo's AI receptionist free, so they never miss a call. You get <b
			>$25 credit</b
		> when they join and take their first job.
	</p>
	<div class="link">
		<span id="plink">{links.p}</span><button type="button" class="cp" onclick={() => copy('p')}
			>{copied.p ? 'Copied' : 'Copy'}</button
		>
	</div>
	<div class="share">
		<button type="button" onclick={() => whatsapp(msgP)}>WhatsApp</button><button type="button" onclick={() => text(msgP)}
			>Text</button
		><button type="button" onclick={() => email(msgP)}>Email</button><button type="button" onclick={() => more(msgP)}
			>More</button
		>
	</div>
	<p class="fine">You send the invite yourself. Scoo never contacts a pro you mention unless they sign up.</p>
</div>
<p class="fine">$10 per friend · $25 per pro · up to $100. Credit applies to requests after launch. Not redeemable for cash.</p>

<style>
	.letmein {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 8px;
		width: 100%;
		text-decoration: none;
		animation: rq-pop 0.5s 0.6s cubic-bezier(0.3, 0.8, 0.3, 1.3) both;
	}
	.letmein svg {
		width: 20px;
		height: 20px;
		fill: none;
		stroke: currentColor;
		stroke-width: 2.2;
		stroke-linecap: round;
		stroke-linejoin: round;
	}
	.meter {
		width: 100%;
		height: 8px;
		border-radius: 99px;
		border: 1.5px solid var(--ink);
		overflow: hidden;
	}
	.meter i {
		display: block;
		height: 100%;
		width: 0;
		background: var(--accent);
		transition: width 1.4s cubic-bezier(0.3, 0.8, 0.3, 1);
	}
	.tabs {
		display: grid;
		grid-template-columns: 1fr 1fr;
		width: 100%;
		border: 1.5px solid var(--ink);
		border-radius: 999px;
		padding: 3px;
		gap: 3px;
	}
	.tabs button {
		min-height: 42px;
		border: 0;
		border-radius: 999px;
		background: transparent;
		color: var(--ink);
		font: 500 15px 'Hanken Grotesk', sans-serif;
		cursor: pointer;
	}
	.tabs button[aria-selected='true'] {
		background: var(--ink);
		color: var(--bg);
	}
	.tab {
		display: flex;
		flex-direction: column;
		gap: 12px;
		width: 100%;
		text-align: left;
	}
	.tab[hidden] {
		display: none;
	}
	.tab p {
		margin: 0;
		line-height: 1.45;
	}
	.link {
		display: flex;
		align-items: center;
		gap: 8px;
		border: 1.5px dashed var(--ink);
		border-radius: 14px;
		padding: 8px 12px;
	}
	.link span {
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.link button {
		flex: 0 0 auto;
		min-height: 38px;
		border-radius: 999px;
		border: 1.5px solid var(--ink);
		background: var(--bg);
		color: var(--ink);
		padding: 0 14px;
		font: 600 14px 'Hanken Grotesk', sans-serif;
		cursor: pointer;
	}
	.share {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 6px;
	}
	.share button {
		min-height: 42px;
		border-radius: 999px;
		border: 1.5px solid var(--ink);
		background: var(--bg);
		color: var(--ink);
		font: 500 14px 'Hanken Grotesk', sans-serif;
		cursor: pointer;
		padding: 0 4px;
	}
	@media (max-width: 420px) {
		.share {
			grid-template-columns: 1fr 1fr;
		}
	}
</style>
