import { FilterButton } from ".";

export const MapSidebar = ({ filterButtons, toggleFilterButtonHandler, toggleAllState, toggleAllHandler }) => {
  return (
    <div className="map-sidebar">
      <button className={"map-filter-button-all"} onClick={toggleAllHandler}>
        <div className="map-filter-button-text">{toggleAllState ?  'Включить все' : 'Выключить все'}</div>
       </button>
      <div className="map-sidebar-filters">
        {filterButtons?.map((fb) => (
          <FilterButton key={`${fb.id}_`} id={fb.id} color={fb.color} isDisabled={fb.isDisabled} toggleHandler={toggleFilterButtonHandler}/>
        ))}
      </div>
    </div>
  );
};

export default MapSidebar;
