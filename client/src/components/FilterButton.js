const FilterButton = ({color, id, isDisabled, toggleHandler}) => {
    return (
        <button className={"map-filter-button" + (isDisabled ? ' disabled' : '')} onClick={() => toggleHandler(id)}>
            <div className="map-filter-button-indicator" style={{backgroundColor: color, width: '10px', height: '10px', borderRadius: '50%'}}></div>
            <div className="map-filter-button-text">#{id}</div>
        </button>
    )
}

export default FilterButton;
