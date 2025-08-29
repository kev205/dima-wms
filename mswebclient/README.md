# DIMA WMS - Telesales Console v1.0.0

A modern Vue 3 frontend application for DIMA Ltd's Warehouse Management System, specifically designed for the telesales team to efficiently manage customer orders, product inventory, and sales operations.

## 🚀 Features

### Core Functionality
- **Customer Management**: Complete CRUD operations for customer data
- **Product Catalog**: Inventory management with stock tracking and availability
- **Sales Orders**: Intuitive order creation with real-time calculations
- **Order Processing**: Draft → Confirmed → Cancelled workflow
- **Inventory Reservations**: Automatic stock reservation on order confirmation

### Telesales Optimized
- **Fast Customer Search**: Instant customer lookup during calls
- **Product Selection**: Quick product search with availability display
- **Price Management**: Flexible pricing with discount support
- **Order Totals**: Real-time calculation with VAT integration
- **Status Tracking**: Visual order status indicators

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Built with Tailwind CSS and Headless UI
- **Real-time Notifications**: Success, error, and warning messages
- **Keyboard Navigation**: Optimized for fast data entry
- **Error Handling**: User-friendly error messages and validation

## 🛠️ Technology Stack

- **Framework**: Vue 3 with Composition API
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for responsive design
- **UI Components**: Headless UI for accessible components
- **Icons**: Heroicons for consistent iconography
- **HTTP Client**: Axios with interceptors
- **State Management**: Pinia for reactive state
- **Routing**: Vue Router with guards
- **Date Handling**: date-fns for formatting
- **Build Tool**: Vite for fast development

## 📁 Project Structure

```
mswebclient/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── AppLayout.vue    # Main application layout
│   │   ├── NotificationList.vue
│   │   ├── LoadingSpinner.vue
│   │   ├── ConfirmDialog.vue
│   │   ├── CustomerFormModal.vue
│   │   ├── ProductFormModal.vue
│   │   ├── CustomerSelector.vue
│   │   └── ProductSelector.vue
│   ├── views/              # Page components
│   │   ├── Dashboard.vue   # Main dashboard
│   │   ├── Products.vue    # Product management
│   │   ├── Customers.vue   # Customer management
│   │   ├── SalesOrders.vue # Order list
│   │   ├── NewSalesOrder.vue # Order creation
│   │   ├── SalesOrderDetail.vue # Order details
│   │   └── Login.vue       # Authentication
│   ├── stores/             # Pinia stores
│   │   ├── auth.ts         # Authentication state
│   │   └── notifications.ts # Notification state
│   ├── services/           # API services
│   │   └── api.ts          # HTTP client and endpoints
│   ├── types/              # TypeScript definitions
│   │   └── index.ts        # Type definitions
│   └── router/             # Vue Router config
│       └── index.ts        # Route definitions
├── public/                 # Static assets
├── index.html             # HTML template
├── package.json           # Dependencies
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind CSS config
└── tsconfig.json          # TypeScript config
```

## 🚦 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Django backend (MSSales) running on `http://localhost:8000`

### Installation

1. **Clone and install dependencies**:
```bash
cd mswebclient
npm install
```

2. **Start development server**:
```bash
npm run dev
```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Default credentials: `admin@example.com` / `adminpass`

### Build for Production

```bash
# Type checking
npm run type-check

# Build optimized bundle
npm run build

# Preview production build
npm run preview
```

## 🔗 API Integration

The frontend connects to the Django backend (MSSales) via REST API:

### Authentication
- JWT token-based authentication
- Auto-refresh and logout on token expiration
- Secure token storage in localStorage

### Endpoints
- `POST /api/auth/login/` - User authentication
- `GET /api/products/` - Product listing with search/pagination
- `POST /api/products/` - Create new product
- `GET /api/customers/` - Customer listing with search
- `POST /api/customers/` - Create new customer
- `GET /api/sales-orders/` - Sales order listing
- `POST /api/sales-orders/` - Create new sales order
- `POST /api/sales-orders/{id}/confirm/` - Confirm order
- `POST /api/sales-orders/{id}/cancel/` - Cancel order

## 🎯 Key Features for Telesales

### Customer Management
- Quick customer search during calls
- Add new customers on-the-fly
- Separate billing/shipping addresses
- Customer history and contact details

### Product Catalog
- Real-time inventory availability
- Quick product search by name
- Price and cost management
- Category organization
- Low stock alerts

### Order Creation Flow
1. **Select Customer**: Search existing or create new
2. **Add Products**: Quick product selection with availability check
3. **Set Quantities**: Real-time availability validation
4. **Apply Discounts**: Line-level discount percentages
5. **Review Totals**: Automatic VAT calculation
6. **Confirm Order**: Reserve inventory and process

### Order Management
- Visual status indicators (Draft/Confirmed/Cancelled)
- Order confirmation with inventory reservation
- Order cancellation with stock release
- Comprehensive order history

## 🎨 Design System

### Color Palette
- **Primary**: Blue (#3B82F6) for main actions
- **Success**: Green (#10B981) for positive states
- **Warning**: Yellow (#F59E0B) for alerts
- **Error**: Red (#EF4444) for errors
- **Neutral**: Gray scale for content

### Component Library
- Consistent button styles (primary, secondary, danger)
- Form inputs with validation states
- Modal dialogs with smooth transitions
- Loading states and spinners
- Toast notifications

## 📱 Responsive Design

- **Mobile First**: Optimized for mobile telesales agents
- **Tablet Support**: Perfect for portable order taking
- **Desktop**: Full-featured dashboard experience
- **Touch Friendly**: Large click targets and gestures

## 🔐 Security Features

- JWT token authentication
- Automatic token refresh
- Secure API communication
- Input validation and sanitization
- CSRF protection ready

## 🧪 Development Features

- **Hot Module Replacement**: Instant updates during development
- **TypeScript**: Full type safety and IntelliSense
- **ESLint**: Code quality and consistency
- **Prettier**: Automatic code formatting
- **Component DevTools**: Vue DevTools support

## 🚀 Performance Optimizations

- **Code Splitting**: Lazy-loaded routes and components
- **Tree Shaking**: Remove unused code
- **Asset Optimization**: Compressed images and fonts
- **Caching**: HTTP response caching
- **Debounced Search**: Reduced API calls

## 🌟 Future Enhancements

- **Offline Support**: PWA capabilities for unreliable connections
- **Real-time Updates**: WebSocket integration for live updates
- **Advanced Reporting**: Sales analytics and dashboards
- **Multi-language**: Internationalization support
- **Print Support**: Order and invoice printing
- **Barcode Scanning**: Mobile barcode integration

## 🤝 Contributing

1. Follow the existing code style and conventions
2. Add TypeScript types for new components
3. Include proper error handling
4. Test responsive design on multiple devices
5. Update documentation for new features

## 📄 License

This project is part of the DIMA WMS system and is proprietary software.

---

**Built with ❤️ for efficient telesales operations**