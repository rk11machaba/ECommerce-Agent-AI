"use client";
import React, { useEffect, useState } from "react";

const Expiring_Products = () => {
  const [expiringProducts, setExpiringProducts] = useState<string>("");
  const [expiredProducts, setExpiredProducts] = useState<string>("")

  useEffect(() => {
    fetch("http://localhost:5000/api/expiring-products")
      .then((response) => response.json())
      .then((data) => {
        // Retrieve data as plain text
        setExpiringProducts(data.expiring_products); //  this is a string
        setExpiredProducts(data.expired_products); // this is another string
      })
      .catch((error) => {
        console.error("Error fetching expiring products:", error);
        setExpiringProducts("Failed to load expiring products.");
      });
  }, []);

return (
    <div className="min-h-screen bg-gradient-to-r from-blue-50 to-blue-100 p-6">
        <h1 className="text-2xl font-bold text-center text-yellow-700 mb-6">
            Product Expiry Dashboard
        </h1>
        <div className="flex flex-row justify-between">
            {/* Expiring Products Section */}
            <div className="w-1/2 p-4">
                <h2 className="text-xl font-bold text-left text-yellow-700 mb-4">
                    Products that are Expiring Soon
                </h2>
                <div className="p-6 bg-white rounded-lg shadow-lg border border-gray-200">
                    <p className="text-gray-700">
                        {expiringProducts || "No expiring products found."}
                    </p>
                </div>
            </div>
            {/* Expired Products Section */}
            <div className="w-1/2 p-4">
                <h2 className="text-xl font-bold text-left text-red-700 mb-4">
                    Expired Products
                </h2>
                <div className="p-6 bg-white rounded-lg shadow-lg border border-gray-200">
                    <p className="text-gray-700">
                        {expiredProducts || "No expired products found."}
                    </p>
                </div>
            </div>
        </div>
    </div>
);
};

export default Expiring_Products;