import React from 'react';

export function DisplayMessage(props) {
  return (
    <div>
      <li class="message">{props.message}</li>
    </div>
  );
}
