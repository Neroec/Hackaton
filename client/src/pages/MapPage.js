import axios from "axios";
import { useEffect, useState } from "react/cjs/react.development";
import { MaskiMap, Preloader } from "../components";
import getRandomColor from "../utils/color-generator";

const MapPage = () => {
  const [roads, setRoads] = useState([]);
  const [isLoadedRoads, setIsLoadedRoads] = useState(false);

  const [edges, setEdges] = useState([]);
  const [isLoadedEdges, setIsLoadedEdges] = useState(false);

  const [componentPositions, setComponentPositions] = useState([]);
  const [isLoadedPositions, setIsLoadedPositions] = useState(false);

  const [filteredComponents, setFilteredComponents] = useState([]);
  const [isLoadedFilteredComponents, setIsLoadedFilteredComponents] =
    useState(false);

  const [toggleAllState, setToggleAllState] = useState(false);

  const toggleFilterHandler = (id) => {
    setFilteredComponents(
      filteredComponents.map((fc) => {
        if (fc.id == id) {
          fc.isDisabled = !fc.isDisabled;
        }

        return fc;
      })
    );
  };

  const toggleAllHandler = () => {
    setFilteredComponents(
      filteredComponents.map((fc) => ({ ...fc, isDisabled: !toggleAllState }))
    );
    setToggleAllState(!toggleAllState);
  };

  useEffect(async () => {
    const resRoads = await axios.get("http://127.0.0.1:5000/roads");
    const roadsEdges = resRoads.data;
    const roadsToSet = [];
    roadsEdges.forEach((e) => roadsToSet.push(e.filter((_, i) => i > 1)));
    setRoads(roadsToSet);
    setIsLoadedRoads(true);

    const resEdges = await axios.get("http://127.0.0.1:5000/edges");
    const edges = resEdges.data;
    setEdges(edges);
    setIsLoadedEdges(true);

    const resRoutes = await axios.get("http://127.0.0.1:5000/routes");
    const routes = resRoutes.data;

    const rts = routes.map((r) => r[1].map((elem) => roadsEdges[elem]));

    const componentPositions = rts.map((t, i) => {
      return {
        positions: t.map((route) => {
          return route.filter((r, i) => i > 1);
        }),
        color: getRandomColor(),
        id: i + 1,
      };
    });

    setComponentPositions(componentPositions);
    setIsLoadedPositions(true);

    setFilteredComponents(
      componentPositions.map((cp, i) => ({
        color: cp.color,
        id: cp.id,
        isDisabled: false,
      }))
    );

    setIsLoadedFilteredComponents(true);
  }, []);

  return (
    <>
      <h1 className="app-title">MaskiMap</h1>
      {isLoadedRoads &&
      isLoadedEdges &&
      isLoadedPositions &&
      isLoadedFilteredComponents ? (
        <MaskiMap
          toggleAllState={toggleAllState}
          toggleAllHandler={toggleAllHandler}
          toggleFilterHandler={toggleFilterHandler}
          roads={roads}
          myComponentPositions={componentPositions}
          filteredComponents={filteredComponents}
        />
      ) : (
        <Preloader />
      )}
    </>
  );
};

export default MapPage;
