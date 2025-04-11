"use client"
import React, { useEffect, useState } from 'react';

const Page = () => {
  const [message, setMessage] = useState("Loading");
  const [expiringProducts, setExpiringProducts] = useState([]);
  const [outOfStockProducts, setOutOfStockProducts] = useState([]);


  useEffect(() => {
    fetch("http://localhost:5000/api/expiring-products")
    .then(
      (response)=>response.json()
    )
    .then((data)=>{
      // retrieve data
      setMessage(data.message);
      setExpiringProducts(data.expiring_products);
      setOutOfStockProducts(data.quantities);
    });
  }, []);

  return(
    <div className='flex flex-col items-center justify-between'>
      <div className='bg-gray-100 p-6 rounded-lg shadow-md text-center'>
        <h1 className='text-2xl font-bold text-gray-800'>
          { message }
        </h1>
      </div>
      <div className=''>
        <h1 className='text-xl font-semibold text-gray-700 mb-4'>Products to Expire</h1>
        <p className='text-gray-600 bg-red-100 p-4 rounded-lg shadow-sm'>
          {
            expiringProducts
          }
        </p>
        <h1 className='text-xl font-semibold text-gray-700 mb-4'>Out of Stock Products</h1>
        <p className='text-gray-600 bg-red-100 p-4 rounded-lg shadow-sm'>
          {
            outOfStockProducts
          }
          ...
        </p>
      </div>
    </div>
  );

}

export default Page