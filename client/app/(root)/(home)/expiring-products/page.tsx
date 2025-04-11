"use client";
import React, { useEffect, useState } from "react";

const Expiring_Products = () => {
  const [expiringProducts, setExpiringProducts] = useState<string>("");

  useEffect(() => {
    fetch("http://localhost:5000/api/expiring-products")
      .then((response) => response.json())
      .then((data) => {
        // Retrieve data as plain text
        setExpiringProducts(data.expiring_products); //  this is a string
      })
      .catch((error) => {
        console.error("Error fetching expiring products:", error);
        setExpiringProducts("Failed to load expiring products.");
      });
  }, []);

  return (
    <div>
      <h1 className="text-lg text-red-700">Products that are expiring soon</h1>
      <div className="flex flex-1 items-center justify-start">
        <p className="p-4 bg-gray-100 rounded-lg shadow-md m-2">
          {expiringProducts || "No expiring products found."}
        </p>
      </div>
    </div>
  );
};

export default Expiring_Products;