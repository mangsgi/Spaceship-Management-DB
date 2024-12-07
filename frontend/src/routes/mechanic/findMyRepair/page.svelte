<script>
    // FindPilotFlight 페이지에 필요한 로직 추가
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import axios from 'axios';

    // 반응형 선언으로 userId 값이 변경될 때마다 pilotId 업데이트
    $: mechanicId = $userId;
    const loading = writable(false);
    let errorMessage = '';

    let data = [];

    async function findMyRepair() {

    loading.set(true);
    

    let endpoint = 'http://localhost:8000/flights_by_pilot';

    try {
      const response = await axios.get(endpoint, { params: { pilot_id: pilotId } });

      // 임시 조건 (실제 응답 검증으로 대체)
      if (response.data && Array.isArray(response.data)) {
        // 역할에 따른 URL로 네비게이션
        data = response.data;
        console.log('결과 : ', data);
        
      } 
    } catch (error) {
      console.error('데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        // 서버 응답 오류 처리
        if (error.response.status === 400) {
          errorMessage = '잘못된 요청입니다. 입력 ID를 확인해주세요.';
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
  <table>
    <thead>
      <tr>
        <th>Flight ID</th>
        <th>Spaceship ID</th>
        <th>Departure Location</th>
        <th>Arrival Location</th>
        <th>Departure Time</th>
        <th>Arrival Time</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      {#each data as flight}
        <tr>
          <td>{flight.flight_id}</td>
          <td>{flight.spaceship_id}</td>
          <td>{flight.departure_location}</td>
          <td>{flight.arrival_location}</td>
          <td>{new Date(flight.departure_time).toLocaleString()}</td>
          <td>{new Date(flight.arrival_time).toLocaleString()}</td>
          <td>{flight.status}</td>
        </tr>
      {/each}
    </tbody>
  </table>
  </div>
  