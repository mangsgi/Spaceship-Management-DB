<!-- src/App.svelte -->
<script>
    import { onMount } from 'svelte';
    import axios from 'axios';

    let items = [];
    let title = '';
    let description = '';

    const fetchItems = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/items/1'); // 예시로 ID 1번 아이템 가져오기
            items = [response.data];
        } catch (error) {
            console.error(error);
        }
    };

    const createItem = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/items/', {
                title,
                description
            });
            items = [...items, response.data];
            title = '';
            description = '';
        } catch (error) {
            console.error(error);
        }
    };

    onMount(() => {
        fetchItems();
    });
</script>

<main>
    <h1>FastAPI & Svelte 프로젝트</h1>

    <h2>아이템 추가</h2>
    <input bind:value={title} placeholder="제목" />
    <input bind:value={description} placeholder="설명" />
    <button on:click={createItem}>추가</button>

    <h2>아이템 목록</h2>
    <ul>
        {#each items as item}
            <li>{item.title}: {item.description}</li>
        {/each}
    </ul>
</main>

<style>
    main {
        padding: 1em;
        max-width: 600px;
        margin: 0 auto;
    }

    input {
        display: block;
        margin-bottom: 0.5em;
        padding: 0.5em;
        width: 100%;
    }

    button {
        padding: 0.5em 1em;
    }

    ul {
        list-style: none;
        padding: 0;
    }

    li {
        padding: 0.5em 0;
        border-bottom: 1px solid #ccc;
    }
</style>
