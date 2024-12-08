<!-- src/routes/pilot/page.svelte -->
<script>
  import { Link, navigate } from 'svelte-routing';
  import { userId } from '../../stores.js'; // stores.js의 경로에 따라 조정

  function navigateHome() {
    navigate('/');
  }

  // 반응형 선언으로 userId 값이 변경될 때마다 pilotId 업데이트
  $: pilotId = $userId;
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap');

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
    width: 300px;
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

<div class="pilot-page">
  <div class="pilot-container">
    <h1>Pilot Page</h1>
    <p>Pilot ID: {pilotId}</p>
    <button on:click={navigateHome}>Main Page</button>

    <h3>Select Your Action</h3>
    <div class="links-container">
      <Link to="/pilot/findPilotFlight"><button>View My Info</button></Link>
      <Link to="/pilot/updatePilotInfo"><button>Update My Info</button></Link>
      <Link to="/pilot/updateLicense"><button>Renew License</button></Link>
    </div>
  </div>
</div>
