<script>
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import axios from 'axios';

  // 반응형 선언으로 userId 값이 변경될 때마다 pilotId 업데이트
  $: pilotId = $userId;
  const loading = writable(false);
  let errorMessage = '';
  let errorMessage_get = '';
  let data_get = null;

  let name = '';
  let contact_info = '';
  let emergency_contact = '';

  async function findMyFlight() {
    loading.set(true);
    errorMessage_get = ''; // 이전 에러 메시지 초기화

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
    console.log('컴포넌트가 마운트되었습니다.');
    findMyFlight();
  });
</script>

<style>
  .page {
    text-align: center;
    padding: 50px;
  }
  button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }
  input {
    margin: 5px;
    padding: 5px;
    font-size: 1em;
  }
  .error {
    color: red;
  }
  .loading {
    font-style: italic;
  }
  table {
    margin: 0 auto;
    border-collapse: collapse;
    width: 80%;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  th {
    background-color: #f2f2f2;
  }
</style>

<div class="page">
  <h2>파일럿 비행 찾기</h2>
  <p>파일럿 ID: {pilotId}</p>

  {#if $loading}
    <p class="loading">로딩 중...</p>
  {/if}

  {#if errorMessage}
    <p class="error">{errorMessage}</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  <!-- 데이터 표시를 위한 테이블 구조 -->
  {#if data_get}
    <h3>파일럿 Info</h3>
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

  <form on:submit|preventDefault={updatePilotInfo}>
    <input type="text" bind:value={name} placeholder="Name" required />
    <input type="text" bind:value={contact_info} placeholder="Contact Info" required />
    <input type="text" bind:value={emergency_contact} placeholder="Emergency Contact" required />
    <button type="submit">파일럿 정보 업데이트</button>
  </form>
</div>
