<script>
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import axios from 'axios';

  // 반응형 선언으로 userId 값이 변경될 때마다 customerId 업데이트
  $: customerId = $userId;

  // 로딩 상태와 에러 메시지 관리
  const loading = writable(false);
  let errorMessage = '';
  let errorMessage_get = '';

  // 비행 필터링 파라미터
  let departure_location = '';
  let arrival_location = '';
  let departure_date = '';
  let sort_by = '';

  // 비행 목록 저장 변수
  let flightData = [];

  // 예약할 비행 선택 변수
  let selectedFlightId = null;

  // 예약 성공 메시지
  let successMessage = '';

  // 비행 일정 필터링 함수
  async function findCustomFlight() {
    loading.set(true);
    errorMessage_get = '';
    successMessage = '';

    const endpoint_get = 'http://localhost:8000/flights_by_customer';

    try {
      const response = await axios.get(endpoint_get, { params: {
        departure_location,
        arrival_location,
        departure_date,
        sort_by
      } });

      // 응답이 배열인지 확인
      if (Array.isArray(response.data)) {
        console.log('Flights:', response.data);
        flightData = response.data;
        if (flightData.length === 0) {
          errorMessage_get = '검색 결과가 없습니다.';
        }
      } else {
        errorMessage_get = '잘못된 응답 형식입니다.';
      }
    } catch (error) {
      console.error('비행 데이터를 가져오는 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage_get = '잘못된 요청입니다. 입력을 확인해주세요.';
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

  // 예약 생성 함수
  async function addReservation() {
    if (!selectedFlightId) {
      errorMessage = '예약할 비행을 선택해주세요.';
      return;
    }

    loading.set(true);
    errorMessage = '';
    successMessage = '';

    const endpoint = `http://localhost:8000/reservations`;

    // 전송할 데이터 정의
    const payload = {
      customer_id: customerId,
      flight_id: selectedFlightId,
      seat_number : "A09"
      // 필요에 따라 추가 필드 삽입
    };

    try {
      const response = await axios.post(endpoint, payload);

      if (response.data) {
        console.log('예약 생성 성공:', response.data);
        successMessage = '예약이 성공적으로 생성되었습니다.';
        // 예약 후 선택 초기화
        selectedFlightId = null;
        // 필요 시 예약 내역을 불러오는 함수 호출
      } else {
        errorMessage = '예약 생성에 실패했습니다.';
      }
    } catch (error) {
      console.error('예약 생성 중 오류 발생:', error);
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = '잘못된 요청입니다. 입력 데이터를 확인해주세요.';
        } else if (error.response.status === 422) {
          errorMessage = '요청을 이해했으나 처리할 수 없습니다.';
        } else if (error.response.status === 404) {
          errorMessage = '해당 비행을 찾을 수 없습니다.';
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

  // 컴포넌트가 마운트될 때 초기화
  onMount(() => {
    console.log('컴포넌트가 마운트되었습니다.');
    // 필요 시 초기 비행 목록을 불러오려면 findCustomFlight() 호출
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
  input, select {
    margin: 5px;
    padding: 5px;
    font-size: 1em;
  }
  .error {
    color: red;
  }
  .success {
    color: green;
  }
  .loading {
    font-style: italic;
  }
  table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 90%;
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
  <h2>비행 예약</h2>
  <p>고객 ID: {customerId}</p>

  {#if $loading}
    <p class="loading">로딩 중...</p>
  {/if}

  {#if errorMessage_get}
    <p class="error">{errorMessage_get}</p>
  {/if}

  {#if successMessage}
    <p class="success">{successMessage}</p>
  {/if}

  <h3>비행 일정 필터링</h3>
  <form on:submit|preventDefault={findCustomFlight}>
    <input type="text" bind:value={departure_location} placeholder="출발지" />
    <input type="text" bind:value={arrival_location} placeholder="도착지" />
    <input type="date" bind:value={departure_date} placeholder="출발 날짜" />
    <select bind:value={sort_by}>
      <option value="">정렬 기준 선택</option>
      <option value="departure_time">출발 날짜</option>
      <option value="arrival_time">도착 날짜</option>
      <!-- 필요에 따라 추가 정렬 옵션 삽입 -->
    </select>
    <button type="submit">비행 검색</button>
  </form>

  {#if flightData.length > 0}
    <h3>검색된 비행</h3>
    <table>
      <thead>
        <tr>
          <th>비행 ID</th>
          <th>출발지</th>
          <th>도착지</th>
          <th>출발 날짜</th>
          <th>도착 날짜</th>
          <th>선택</th>
        </tr>
      </thead>
      <tbody>
        {#each flightData as flight}
          <tr>
            <td>{flight.flight_id}</td>
            <td>{flight.departure_location}</td>
            <td>{flight.arrival_location}</td>
            <td>{new Date(flight.departure_date).toLocaleString()}</td>
            <td>{new Date(flight.arrival_date).toLocaleString()}</td>
            <td>
              <input type="radio" name="selectedFlight" bind:group={selectedFlightId} value={flight.flight_id} />
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
    <button on:click={addReservation}>예약 생성</button>
  {/if}

  {#if errorMessage}
    <p class="error">{errorMessage}</p>
  {/if}
</div>
