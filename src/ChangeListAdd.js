import React from 'react';

export function ChangeListAdd(props) {
  return (
    <li>
      {props.method}: {props.artist_id}
    </li>
  );
}
