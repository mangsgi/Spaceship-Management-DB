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

.customer-container {
    background-color: rgba(0, 0, 0, 0.6); /* 반투명 배경 */
    padding: 40px;
    border-radius: 20px;
    width: 300px;
  }
  .customer-page button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }

  h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 2em;
    margin-bottom: 20px;
  }

  h2 {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5em;
    margin-bottom: 20px;
  }

  h3 {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.2em;
    margin-bottom: 20px;
  }

  p {
    font-family: 'Orbitron', sans-serif;
    font-size: 1em;
    margin-bottom: 20px;
  }

  button, .button-link {
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
    text-decoration: none; /* Link 스타일 초기화 */
    display: inline-block;
    text-align: center;
  }

  button:hover, .button-link:hover {
    background-color: white;
    color: black;
  }

  .links-container {
    display: flex;
    flex-direction: column;
  }

  .links-container button {
    width: 100%;
    margin: 5px 0;
  }
</style>

<div class="customer-page">
  <div class="customer-container">
  <h2>Customer Page</h2>
  <p>Customer ID: {customerId}</p>
  <button on:click={navigateHome}>Main Page</button>

  <div>
    <h3>Select Your Action</h3>
    <Link to="/customer/findFlightsAndAddReservation">
      <button>Flight Reservation & Search Flight Schedule</button>
    </Link>
    <Link to="/customer/findMyReservationAndCancel">
      <button>My Reservation & Cancel</button>
    </Link>
    <Link to="/customer/updateCustomInfo">
      <button>Update My Info</button>
    </Link>
  </div>
</div>
</div>
