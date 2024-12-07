<script>
  // updatePilotInfo 페이지에 필요한 로직 추가
import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
import { onMount } from 'svelte';
import { writable } from 'svelte/store';
import axios from 'axios';

  // 반응형 선언으로 userId 값이 변경될 때마다 pilotId 업데이트
  $: pilotId = $userId;
  const loading = writable(false);
  let errorMessage = '';
  let data= [];
  let errorMessage_get = '';
  let data_get= {};

  let name = '';
  let contact_info = '';
  let emergency_contact = '';

  async function findMyFlight() {

  loading.set(true);

  let endpoint_get = 'http://localhost:8000/pilots';

  try {
    const response = await axios.get(endpoint_get, { params: { pilot_id: pilotId } });

    // 임시 조건 (실제 응답 검증으로 대체)
    if (response.data && response.data.pilot_id === pilotId) {
      // 역할에 따른 URL로 네비게이션
      data_get = response.data;
      
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

  async function updatePilotInfo() {

  loading.set(true);
  errorMessage = '';
  
  //여기부터
  const endpoint = `http://localhost:8000/pilots/${pilotId}`;

  // 전송할 데이터 정의 (예: 업데이트할 파일럿 정보)
  const payload = {
    name,
    contact_info,
    emergency_contact,
  };

  try {
    const response = await axios.patch(endpoint, payload);

    // 임시 조건 (실제 응답 검증으로 대체)
    if (response.data) {
      data.push(response.data); // 새로 업데이트된 비행 정보를 data 배열에 추가
      console.log('결과:', response.data);
      data_get = response.data;
    } else {
      console.log('Received data:', response.data);
      errorMessage = '일치하는 데이터를 찾을 수 없습니다.';
    }
  } catch (error) {
    console.error('데이터를 가져오는 중 오류 발생:', error);
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
      // 여기에 초기화 코드나 데이터 페칭 코드를 추가할 수 있습니다.
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
</style>

<div class="page">
  <h2>파일럿 비행 찾기</h2>
  <p>파일럿 ID: {pilotId}</p>
  <!-- 하위 페이지 내용 추가 -->

  <!-- 데이터 표시를 위한 테이블 구조 -->
  <form on:submit|preventDefault={updatePilotInfo}>
    <input type="text" bind:value={name} placeholder="Name" required />
    <input type="text" bind:value={contact_info} placeholder="Contact Info" required />
    <input type="text" bind:value={emergency_contact} placeholder="Emergency Contact" required />
    <button type="submit">파일럿 정보 업데이트</button>
  </form>

  <h3>파일럿 info</h3>
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
</div>
