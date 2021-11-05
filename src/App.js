import './App.css';
import { useState, useRef } from 'react';
import { ChangeListAdd } from './ChangeListAdd.js';
import { DisplayMessage } from './DisplayMessage.js';

function App() {
  const args = JSON.parse(document.getElementById('data').text);

  const [methods, setMethods] = useState([]);
  const [artistChanges, setArtistChanges] = useState([]);
  const [warnings, setWarnings] = useState([]);
  const [successes, setSuccesses] = useState([]);
  const [artistIdsAdded, setArtistIdsAdded] = useState([]);
  const [artistNamesAdded, setArtistNamesAdded] = useState([]);
  const artistIDInput = useRef(null);

  function onAddClick() {
    let newArtist = artistIDInput.current.value;
    if (newArtist) {
      let newMethods = [...methods, 'add'];
      setMethods(newMethods);
      let newArtists = [...artistChanges, newArtist];
      setArtistChanges(newArtists);
    }
    artistIDInput.current.value = '';
  }

  function onRemoveClick(artist) {
    let newMethods = [...methods, 'delete'];
    setMethods(newMethods);
    let newArtists = [...artistChanges, artist];
    setArtistChanges(newArtists);
    let line = document.getElementById(artist);
    line.parentNode.removeChild(line);
  }

  function onSaveClick() {
    let data = {
      methods: methods,
      artist_changes: artistChanges,
    };
    fetch('/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setMethods([]);
        setArtistChanges([]);
        setSuccesses(data.successes);
        setWarnings(data.warnings);
        setArtistIdsAdded(data.added_ids);
        setArtistNamesAdded(data.added_names);
      });
  }

  return (
    <>
      <h1>{args.current_user}'s Song Explorer</h1>
      {args.are_artists_saved ? (
        <>
          <h2>{args.track_name}</h2>
          <h3>{args.track_artist}</h3>
          <div>
            <img src={args.track_album_link} width={300} height={300} />
          </div>
          <div>
            <audio controls>
              <source src={args.track_preview} />
            </audio>
          </div>
          <a href={args.genius_link}> Click here to see lyrics! </a>
          <ul>
            <h3>Currently Saved Artists:</h3>
            {Object.keys(args.artists_saved).map((artist) => (
              <li id={artist}>
                {args.artists_saved[artist]}: {artist}
                <button onClick={() => onRemoveClick(artist)}>Remove</button>
              </li>
            ))}
            {artistIdsAdded.map((artist, index) => (
              <li id={artist}>
                {artistNamesAdded[index]}: {artist}
                <button onClick={() => onRemoveClick(artist)}>Remove</button>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <h2>Looks like you don't have anything saved! Use the form below!</h2>
      )}
      <h1>Save a favorite artist ID for later:</h1>
      <div>
        <input
          type="text"
          placeholder="Add a new artist's ID"
          ref={artistIDInput}
          name="artist_id"
        />
        <button onClick={onAddClick}>Add a new artist</button>
      </div>
      <h3>
        Staged Changes <button onClick={onSaveClick}>Save Changes</button>
      </h3>
      <p>
        <b>Format:</b> Pending method: Artist ID
      </p>
      <ul>
        {methods.map((item, index) => (
          <ChangeListAdd method={item} artist_id={artistChanges[index]} />
        ))}
      </ul>
      <ul class="success">
        {successes.map((item) => (
          <DisplayMessage message={item} />
        ))}
      </ul>
      <ul class="warning">
        {warnings.map((item) => (
          <DisplayMessage message={item} />
        ))}
      </ul>
    </>
  );
}

export default App;
