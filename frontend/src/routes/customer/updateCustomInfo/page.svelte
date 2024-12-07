<script>
  // updatePilotInfo 페이지에 필요한 로직 추가
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import axios from 'axios';

  // 반응형 선언으로 userId 값이 변경될 때마다 customerId 업데이트
  $: customerId = $userId;
  const loading = writable(false);
  let errorMessage = '';
  let errorMessage_get = '';
  let data_get = null; // 초기값을 null로 설정

  let name = '';
  let contact_info = '';

  async function findMyInfo() {
    loading.set(true);
    errorMessage_get = '';

    const endpoint_get = 'http://localhost:8000/customers';

    try {
      const response = await axios.get(endpoint_get, { params: { customer_id: customerId } });

      // 응답이 배열인지 확인
      if (Array.isArray(response.data)) {
        const matchedItem = response.data.find(item => item.customer_id === customerId);
        if (matchedItem) {
          console.log('결과:', matchedItem);
          data_get = matchedItem; // 배열이 아닌 객체로 설정
        } else {
          errorMessage_get = '해당 고객을 찾을 수 없습니다.';
        }
      } else {
        errorMessage_get = '잘못된 응답 형식입니다.';
      }
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        // 서버 응답 오류 처리
        if (error.response.status === 400) {
          errorMessage_get = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
        } else {
          errorMessage_get = `서버 오류 발생: ${error.response.status}`;
        }
      } else {
        // 요청이 서버에 도달하지 못한 경우
        errorMessage_get = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  async function updateMyInfo() {
    loading.set(true);
    errorMessage = '';

    const endpoint = `http://localhost:8000/customers/${customerId}`;

    // 전송할 데이터 정의 (예: 업데이트할 파일럿 정보)
    const payload = {
      name,
      contact_info
    };

    try {
      const response = await axios.patch(endpoint, payload);

      // 업데이트 성공 시 data_get을 업데이트된 객체로 설정
      if (response.data) {
        data_get = response.data;
        console.log('업데이트 결과:', response.data);
      } else {
        errorMessage = '일치하는 데이터를 찾을 수 없습니다.';
      }
    } catch (error) {
      console.error('데이터 업데이트 중 오류 발생:', error);
      if (error.response) {
        // 서버 응답 오류 처리
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
        // 요청이 서버에 도달하지 못한 경우
        errorMessage = '서버에 연결할 수 없습니다.';
      }
    } finally {
      loading.set(false);
    }
  }

  onMount(() => {
    console.log('컴포넌트가 마운트되었습니다.');
    // 초기화 코드나 데이터 페칭 코드 추가
    findMyInfo();
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
</style>

<div class="page">
  <h2>본인 정보 수정</h2>
  <p>고객 ID: {customerId}</p>

  {#if $loading}
    <p class="loading">로딩 중...</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  <!-- 데이터 표시를 위한 테이블 구조 -->
  {#if data_get}
    <form on:submit|preventDefault={updateMyInfo}>
      <input type="text" bind:value={name} placeholder="Name" required />
      <input type="text" bind:value={contact_info} placeholder="Contact Info" required />
      <button type="submit">고객 정보 업데이트</button>
    </form>

    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}

    <h3>My info</h3>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Contact Info</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{data_get.name}</td>
          <td>{data_get.contact_info}</td>
        </tr>
      </tbody>
    </table>
  {/if}
</div>
