import React, { useState, useEffect } from 'react';
import { ShoppingCart, User, Search, Smile, Tag, DollarSign } from 'lucide-react';

// Main App component
const App = () => {
  const [sweets, setSweets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  // Fetch sweet data from a mock API
  useEffect(() => {
    const fetchSweets = async () => {
      try {
        // Fetch from a mock API for demonstration purposes. In a real application, this would point to your backend.
        const response = await fetch('https://fakestoreapi.com/products?limit=12'); 
        if (!response.ok) {
          throw new Error('Failed to fetch sweets');
        }
        const data = await response.json();
        // Adapt the mock API data to a sweet shop format
        const sweetData = data.map(item => ({
          id: item.id,
          name: item.title,
          category: item.category,
          price: item.price,
          description: item.description,
          image: item.image,
        }));
        setSweets(sweetData);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchSweets();
  }, []);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredSweets = sweets.filter(sweet =>
    sweet.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    sweet.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50 font-inter">
      {/* Header */}
      <header className="p-4 bg-white shadow-lg flex flex-col sm:flex-row justify-between items-center sticky top-0 z-10">
        <div className="flex items-center mb-4 sm:mb-0">
          <h1 className="text-3xl font-bold text-pink-600">Sweetopia</h1>
          <Smile className="text-pink-500 ml-2" />
        </div>
        <div className="flex items-center space-x-4">
          <div className="relative w-full sm:w-64">
            <input
              type="text"
              placeholder="Search sweets..."
              value={searchTerm}
              onChange={handleSearch}
              className="w-full border border-gray-300 rounded-full px-4 py-2 pl-10 focus:outline-none focus:ring-2 focus:ring-pink-500 transition-shadow"
            />
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          </div>
          <button className="p-3 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition-colors">
            <User size={20} />
          </button>
          <button className="relative p-3 bg-pink-500 text-white rounded-full hover:bg-pink-600 transition-colors">
            <ShoppingCart size={20} />
            <span className="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-red-100 transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">0</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">Our Sweet Selection</h2>
        {loading && (
          <div className="text-center text-gray-500 text-lg">Loading sweets...</div>
        )}
        {error && (
          <div className="text-center text-red-500 text-lg">Error: {error}</div>
        )}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredSweets.map((sweet) => (
            <div key={sweet.id} className="bg-white p-4 rounded-xl shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 cursor-pointer">
              <img src={sweet.image} alt={sweet.name} className="w-full h-48 object-cover rounded-lg mb-4" />
              <h3 className="font-bold text-xl text-gray-900 mb-1 truncate">{sweet.name}</h3>
              <p className="text-gray-600 text-sm flex items-center mb-2"><Tag size={16} className="mr-1 text-pink-400" /> {sweet.category}</p>
              <div className="flex items-center justify-between">
                <p className="text-green-600 font-bold text-2xl flex items-center"><DollarSign size={20} />{sweet.price.toFixed(2)}</p>
                <button className="px-4 py-2 bg-pink-500 text-white font-semibold rounded-full hover:bg-pink-600 transition-all">
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="p-6 bg-gray-800 text-white text-center rounded-t-lg">
        <p>&copy; 2023 Sweetopia. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default App;
