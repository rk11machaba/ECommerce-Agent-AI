"use client"
import React, { useEffect, useState } from 'react';

const Page = () => {
  const [message, setMessage] = useState("Loading");
  const [items, setItems] = useState([])

  useEffect(() => {
    fetch("http://localhost:5000/api/home")
    .then(
      (response)=>response.json()
    )
    .then((data)=>{
      // retrieve data
      setMessage(data.message);
      setItems(data.items);

    });
  }, []);

  return(
    <div className='flex flex-col items-center justify-between'>
      <div className='bg-gray'>{ message }</div>
      <div>
        {
          items.map((item, index) =>(
            <div key={index}>{ item }</div>
          ))
        }
      </div>
    </div>
  );

}

export default Page