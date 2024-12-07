<script>
  import { Link, navigate } from 'svelte-routing';
  import { userId } from '../../stores.js'; // stores.js의 경로에 따라 조정

  function navigateHome() {
    navigate('/');
  }

  $: customerId = $userId;
</script>

<style>
  .customer-page {
    text-align: center;
    padding: 50px;
  }
  .customer-page button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }
  button {
    margin-top: 20px;
    padding: 10px 20px;
    cursor: pointer;
  }
</style>

<div class="customer-page">
  <h2>정비사 페이지</h2>
  <p>정비사 ID: {customerId}</p>
  <button on:click={navigateHome}>홈으로 돌아가기</button>
  <!-- 정비사 관련 내용 추가 -->

  <div>
    <h3>골라 들어가기</h3>
    <Link to="/customer/findFlightsAndAddReservation">
      <button>본인 예약 생성 & 비행일정 조회</button>
    </Link>
    <Link to="/customer/findMyReservationAndCancel">
      <button>예약 조회 및 취소</button>
    </Link>
    <Link to="/customer/updateCustomInfo">
      <button>본인 정보 수정</button>
    </Link>
  </div>
</div>
