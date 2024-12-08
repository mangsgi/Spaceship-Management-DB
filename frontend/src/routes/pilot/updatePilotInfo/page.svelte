<!-- src/routes/pilot/updatePilotInfo.svelte -->
<script>
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import axios from 'axios';
  import { navigate } from 'svelte-routing';

  let pilotId;
  $: pilotId = $userId;

  const loading = writable(false);
  let errorMessage = '';
  let errorMessage_get = '';
  let data_get = null;

  let name = '';
  let contact_info = '';
  let emergency_contact = '';

  async function findMyPilotInfo() {
    loading.set(true);
    errorMessage_get = '';

    const endpoint_get = 'http://localhost:8000/pilots';

    try {
      const response = await axios.get(endpoint_get, { params: { pilot_id: pilotId } });

      if (Array.isArray(response.data)) {
        const matchedItem = response.data.find(item => item.pilot_id === pilotId);
        if (matchedItem) {
          console.log('결과:', matchedItem);
          data_get = matchedItem;
        } else {
          errorMessage_get = '해당 조종사를 찾을 수 없습니다.';
        }
      } else {
        errorMessage_get = '잘못된 응답 형식입니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_get = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
        } else {
          errorMessage_get = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage_get = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  async function updatePilotInfo() {
    loading.set(true);
    errorMessage = '';

    const endpoint = `http://localhost:8000/pilots/${pilotId}`;

    const payload = {
      name,
      contact_info,
      emergency_contact,
    };

    try {
      const response = await axios.patch(endpoint, payload);

      if (response.data) {
        data_get = response.data;
        console.log('업데이트 결과:', response.data);
        alert('파일럿 정보가 성공적으로 업데이트되었습니다.');
        // 입력 필드 초기화
        name = '';
        contact_info = '';
        emergency_contact = '';
      } else {
        errorMessage = '일치하는 데이터를 찾을 수 없습니다.';
      }
    } catch (error) {
      console.error('데이터를 업데이트하는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = '잘못된 요청입니다. 입력 데이터를 확인해주세요.';
        } else if (error.response.status === 422) {
          errorMessage = '서버가 요청을 이해했으나 처리할 수 없습니다. 요청 데이터를 확인해주세요.';
        } else if (error.response.status === 404) {
          errorMessage = '해당 파일럿을 찾을 수 없습니다.';
        } else {
          errorMessage = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        errorMessage = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  onMount(() => {
    console.log('파일럿 정보 업데이트 컴포넌트가 마운트되었습니다.');
    findMyPilotInfo();
  });
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Orbitron:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  .pilot-page {
  position: absolute; /* 또는 fixed */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  
  text-align: center;
  padding: 0; /* 패딩 제거 */
  background-image: url('/images/space_main.png'); /* 원하는 배경 이미지 경로 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat; /* 배경 이미지 반복 방지 */
  background-attachment: fixed; /* 배경 이미지 고정 */
  color: white;
  width: 100vw; /* 전체 뷰포트 너비의 120% */
  height: 120vh; /* 전체 뷰포트 높이의 120% */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: 'Orbitron', sans-serif;
  overflow: hidden; /* 필요에 따라 추가 */
}


  .pilot-container {
    background-color: rgba(0, 0, 0, 0.6); /* 반투명 배경 */
    padding: 40px;
    border-radius: 20px;
    width: 80%;
    max-width: 800px;
  }

  h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
  }

  h1 {
    font-size: 3em;
    margin-bottom: 20px;
  }

  h2 {
    font-size: 2em;
    margin-bottom: 20px;
  }

  h3 {
    font-size: 1.5em;
    margin-bottom: 20px;
  }

  p {
    font-family: 'Orbitron', sans-serif;
    font-size: 1em;
    margin-bottom: 20px;
  }

  form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input[type="text"] {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 2px solid white;
    border-radius: 10px;
    background-color: transparent;
    color: white;
    font-family: 'Orbitron', sans-serif;
    font-size: 1em;
  }

  input::placeholder {
    color: #ccc;
  }

  button {
    font-family: 'Orbitron', sans-serif;
    font-size: 1em;
    margin: 10px 0;
    padding: 10px 20px;
    border-radius: 50px;
    border: 2px solid white;
    background-color: transparent;
    color: white;
    transition: background-color 0.3s, color 0.3s;
    width: 100%;
    cursor: pointer;
  }

  button:hover {
    background-color: white;
    color: black;
  }

  table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 100%;
    color: white;
  }

  th, td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: left;
  }

  th {
    background: #333;
  }

  tbody {
    background-color: rgba(0, 0, 0, 0.5); /* White with 80% opacity */
}

  .loading {
    font-style: italic;
    margin-top: 10px;
  }

  .error {
    color: #ffcccc;
    font-size: 1em;
    margin-top: 10px;
  }

  .home-button {
    width: auto;
    margin: 10px 0;
  }
</style>

<div class="pilot-page">
  <div class="pilot-container">
    <h1>Update Pilot Info</h1>
    <p>Pilot ID: {pilotId}</p>
    <button on:click={() => navigate('/pilot')}>Back to Menu
    </button>

    {#if $loading}
      <p class="loading">Loading...</p>
    {/if}

    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}

    {#if errorMessage_get}
      <p class="error">{errorMessage_get}</p>
    {/if}

    {#if data_get}
      <h2>Now Pilot Info</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Contact Info</th>
            <th>Emergency Contact</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{data_get.name}</td>
            <td>{data_get.contact_info}</td>
            <td>{data_get.emergency_contact}</td>
          </tr>
        </tbody>
      </table>
    {:else if !errorMessage_get && !$loading}
      <p>No data available.</p>
    {/if}

    <h2>Update Pilot Info</h2>
    <form on:submit|preventDefault={updatePilotInfo}>
      <input type="text" bind:value={name} placeholder="Name" required />
      <input type="text" bind:value={contact_info} placeholder="Contact Info" required />
      <input type="text" bind:value={emergency_contact} placeholder="Emergency Contact" required />
      <button type="submit">Update</button>
    </form>
  </div>
</div>
