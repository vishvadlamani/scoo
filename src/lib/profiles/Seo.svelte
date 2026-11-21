<!-- Title, description and share tags for a page; `index: false` keeps it out of search results. -->
<script lang="ts">
	let {
		title,
		description,
		path,
		index = true,
		jsonLd = null
	}: { title: string; description: string; path: string; index?: boolean; jsonLd?: Record<string, unknown> | null } = $props();

	const url = $derived(`https://scoo.app${path}`);
	// Escaped so a business name can never close the script tag it sits in.
	const ld = $derived(jsonLd ? JSON.stringify(jsonLd).replace(/</g, '\\u003c') : '');
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="description" content={description} />
	<link rel="canonical" href={url} />
	<meta property="og:type" content="website" />
	<meta property="og:site_name" content="Scoo" />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={description} />
	<meta property="og:url" content={url} />
	<meta name="twitter:card" content="summary" />
	{#if !index}<meta name="robots" content="noindex" />{/if}
	{#if ld}{@html `<script type="application/ld+json">${ld}</script>`}{/if}
</svelte:head>
