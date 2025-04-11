"use client";
import React, { useEffect, useState } from "react";

const Page = () => {
  interface Product {
    name: string;
    brand: string;
    price: number;
    quantity: number;
    expiring_date: string;
  }
  
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/products")
      .then((response) => response.json())
      .then((data) => {
        // Retrieve data
        setProducts(data.products);
      });
  }, []);

  // Separate products into "In Stock" and "Out of Stock"
  const inStockProducts = products.filter((product) => product.quantity > 0);
  const outOfStockProducts = products.filter((product) => product.quantity === 0);

  return (
    <div>
      <div className="flex flex-col items-center justify-between"></div>
      <div className="bg-gray-100 p-6 rounded-lg shadow-md text-center">
        <h1 className="text-2xl font-bold text-gray-800">Product List</h1>
      </div>
      <div className="flex w-full mt-6">
        {/* In Stock Products */}
        <div className="w-1/2 pr-4">
          <h1 className="text-xl font-semibold text-gray-700 mb-4">In Stock</h1>
          <div className="text-gray-600 bg-green-100 p-4 rounded-lg shadow-sm">
            {inStockProducts.length > 0 ? (
              inStockProducts.map((product, index) => (
                <div key={index} className="mb-2">
                  <p>
                    <strong>Name:</strong> {product.name}
                  </p>
                  <p>
                    <strong>Brand:</strong> {product.brand}
                  </p>
                  <p>
                    <strong>Price:</strong> ${product.price}
                  </p>
                  <p>
                    <strong>Quantity:</strong> {product.quantity}
                  </p>
                  <p>
                    <strong>Expiring Date:</strong> {product.expiring_date}
                  </p>
                  <hr className="my-2" />
                </div>
              ))
            ) : (
              <p>No products in stock.</p>
            )}
          </div>
        </div>

        {/* Out of Stock Products */}
        <div className="w-1/2 pl-4">
          <h1 className="text-xl font-semibold text-gray-700 mb-4">Out of Stock Products</h1>
          <div className="text-gray-600 bg-red-100 p-4 rounded-lg shadow-sm">
            {outOfStockProducts.length > 0 ? (
              outOfStockProducts.map((product, index) => (
                <div key={index} className="mb-2">
                  <p>
                    <strong>Name:</strong> {product.name}
                  </p>
                  <p>
                    <strong>Brand:</strong> {product.brand}
                  </p>
                  <p>
                    <strong>Price:</strong> ${product.price}
                  </p>
                  <p>
                    <strong>Expiring Date:</strong> {product.expiring_date}
                  </p>
                  <hr className="my-2" />
                </div>
              ))
            ) : (
              <p>All products are in stock.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Page;