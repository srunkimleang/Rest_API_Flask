import React from 'react';
function UserList(props) {
    return (
        <div>
            {props.users && props.users.map(user => {
                return (
                    <div key= {user.id}>
                        <h2>{user.name}</h2>
                        <p>{user.email}</p>
                        <p>{user.id}</p>
                    </div>
                )
            })}
        </div>
    );
}

export default UserList;