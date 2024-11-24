<!-- src/App.svelte -->
<script>
    import { onMount } from 'svelte';
    import axios from 'axios';

    let pilots = [];
    let pilot_id = '';
    let name = '';
    let contact_info = '';
    let emergency_contact = '';
    let license_number = '';
    let license_expiry_date = '';

    const fetchItems = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/pilots/1'); // 예시로 ID 1번 아이템 가져오기
            pilots = [response.data];
        } catch (error) {
            console.error(error);
        }
    };

    //수정 필요, api에서 pilots/ 라는 get을 하나 추가해야한다.
    const fetchAllPilots = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/pilots/');
            console.log(response.data); // 데이터 확인용 로그
            pilots = response.data; // response.data가 배열인지 확인
            console.log(pilots);
        } catch (error) {
            console.error(error);
        }
    };

    const createItem = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/pilots/', {
                pilot_id,
                name,
                contact_info,
                emergency_contact,
                license_number,
                license_expiry_date
            });
            pilots = [...pilots, response.data];
            pilot_id = '';
            name = '';
            contact_info = '';
            emergency_contact = '';
            license_number = '';
            license_expiry_date = '';
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
    <input bind:value={pilot_id} placeholder="ID" />
    <input bind:value={name} placeholder="이름" />
    <input bind:value={contact_info} placeholder="info" />
    <input bind:value={emergency_contact} placeholder="emergency_contact" />
    <input bind:value={license_number} placeholder="license_number" />
    <input bind:value={license_expiry_date} placeholder="license_expiry_date" />
    <button on:click={createItem}>추가</button>

    <h2>아이템 목록</h2>
    <ul>
        {#each pilots as pilot}
            <li>{pilot.name}: {pilot.contact_info}</li>
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
