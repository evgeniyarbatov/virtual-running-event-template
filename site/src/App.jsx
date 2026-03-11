import Intro from './components/Intro';
import Map from './components/Map';
import Status from './components/Status';
import Progress from './components/Progress';
import Log from './components/Log';

function App() {
  return (
    <div className="app">
      <section id="intro" className="snap-section min-vh-100 d-flex align-items-center justify-content-center bg-light">
        <div style={{ width: '600px' }} className="text-justify">
          <Intro />
        </div>
      </section>
      <section id="map" className="snap-section min-vh-100">
        <div style={{ height: '100%', width: '100%' }}>
          <Map />
        </div>
      </section>
      <section id="status" className="snap-section min-vh-100 d-flex align-items-center justify-content-center bg-light">
        <div style={{ width: '600px' }} className="text-justify">
          <Status />
        </div>
      </section>
      <section id="status" className="snap-section min-vh-100 d-flex align-items-center justify-content-center bg-light">
        <div style={{ width: '600px' }} className="text-justify">
          <Progress />
        </div>
      </section>
      <section id="log" className="snap-section min-vh-100 d-flex align-items-center justify-content-center bg-light">
        <div style={{ width: '600px' }} className="text-justify">
          <Log />
        </div>
      </section>

    </div>
  );
}

export default App;
