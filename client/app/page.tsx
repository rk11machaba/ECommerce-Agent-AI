"use client"
import React, { useEffect, useState } from 'react'

const page = () => {
  const [message, setMessage] = useState("loading");
  const [items, setItems] = useState([])

  useEffect(() => {
    fetch("http://localhost:8080/api/home")
    .then(
      (response)=>response.json()
    )
    .then((data)=>{
      // retrieve data
      setMessage(data.message);
      setItems(data.items);

      console.log(data.message)
      console.log(data.items);
    });
  }, []);

  return(
    <div>
      <div>{ message }</div>
      {
        items.map((item, index) =>(
          <div key={index}>{ item }</div>
        ))
      }
    </div>
  );

}

export default page