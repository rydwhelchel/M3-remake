import './App.css';
import { useState, useRef } from 'react';
import Button from 'react-bootstrap/Button';
import ListGroup from 'react-bootstrap/ListGroup';
import { InputGroup, ListGroupItem } from 'react-bootstrap';
import { Image } from 'react-bootstrap';
import { FormControl } from 'react-bootstrap';
import './static/List.css';

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

  function onLogoutClick() {
    fetch('/logout', {
      method: 'POST',
    });
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
    <div className="super-grid">
      <h1>
        {args.current_user}'s Song Explorer{' '}
        <Button type="submit" variant="outline-danger" onClick={onLogoutClick}>
          Logout
        </Button>
        <p style={{ fontSize: 'small' }}>please refresh after clicking</p>
      </h1>
      <div className="wrapper-grid">
        <div>
          {args.are_artists_saved ? (
            <>
              <h2>{args.track_name}</h2>
              <h3>{args.track_artist}</h3>
              <div>
                <Image
                  src={args.track_album_link}
                  width={300}
                  height={300}
                  rounded
                />
              </div>
              <div>
                <audio controls>
                  <source src={args.track_preview} />
                </audio>
              </div>
              <a href={args.genius_link}> Click here to see lyrics! </a>
            </>
          ) : (
            <h2>
              Looks like you don't have anything saved! Use the form below!
            </h2>
          )}
        </div>
        <div>
          <ListGroup variant="flush" as="ol" numbered>
            <h3>Currently Saved Artists:</h3>
            {args.are_artists_saved ? (
              <>
                {Object.keys(args.artists_saved).map((artist) => (
                  <ListGroup.Item as="li" className="listItem" id={artist}>
                    {args.artists_saved[artist]}: {artist}
                    <Button
                      variant="outline-danger"
                      onClick={() => onRemoveClick(artist)}
                    >
                      Remove
                    </Button>
                  </ListGroup.Item>
                ))}
                {artistIdsAdded.map((artist, index) => (
                  <ListGroup.Item as="li" className="listItem" id={artist}>
                    {artistNamesAdded[index]}: {artist}
                    <Button
                      variant="outline-danger"
                      onClick={() => onRemoveClick(artist)}
                    >
                      Remove
                    </Button>
                  </ListGroup.Item>
                ))}
              </>
            ) : (
              <></>
            )}
          </ListGroup>
          <h1>Save a favorite artist ID for later:</h1>
          <ListGroup variant="flush">
            <InputGroup style={{ width: '100%' }}>
              <FormControl
                type="text"
                style={{ width: '1fr' }}
                placeholder="Add a new artist's ID"
                ref={artistIDInput}
                name="artist_id"
              />
              <Button onClick={onAddClick}>Add a new artist</Button>
            </InputGroup>
            <ListGroup.Item variant="flush" className="listItem">
              Staged Changes <Button onClick={onSaveClick}>Save Changes</Button>
            </ListGroup.Item>
          </ListGroup>
          <p>
            <b>Format:</b> Pending method: Artist ID
          </p>
          <ListGroup>
            {methods.map((item, index) =>
              item === 'add' ? (
                <ListGroup.Item variant="success">
                  {item} : {artistChanges[index]}
                </ListGroup.Item>
              ) : (
                <ListGroup.Item variant="danger">
                  {item} : {artistChanges[index]}
                </ListGroup.Item>
              )
            )}
            {successes.map((item) => (
              <ListGroup.Item variant="success">{item}</ListGroup.Item>
            ))}
            {warnings.map((item) => (
              <ListGroup.Item variant="danger">{item}</ListGroup.Item>
            ))}
          </ListGroup>
        </div>
      </div>
    </div>
  );
}

export default App;
