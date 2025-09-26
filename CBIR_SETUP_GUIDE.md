# 🏠 CBIR Database Setup Guide

This guide will help you add 50+ house records to your database for better CBIR functionality.

## 📋 What You'll Get

- **50+ Houses** with realistic Thai names and descriptions
- **15 Projects** in different Thai locations
- **5 House Types** (บ้านสองชั้น, บ้านชั้นเดียว, บ้านวิลล่า, ทาวน์เฮาส์, บ้านแฝด)
- **32 House Features** (สระว่ายน้ำ, สวนสวย, ที่จอดรถ, etc.)
- **Updated CBIR Features** for all house images
- **Enhanced Search Results** with many more similar houses

## 🚀 Quick Setup (Automated)

### Option 1: Run the Complete Setup Script
```bash
python setup_cbir_database.py
```

This will:
1. Check MySQL connection
2. Import house data
3. Update CBIR features
4. Test the system

## 🔧 Manual Setup (Step by Step)

### Step 1: Start MySQL Server
Make sure your MySQL server is running.

### Step 2: Import House Data
```bash
# Method 1: Using MySQL command line
mysql -u root -p projectdb < add_house_data.sql

# Method 2: Using phpMyAdmin
# 1. Open phpMyAdmin
# 2. Select 'projectdb' database
# 3. Go to 'Import' tab
# 4. Choose 'add_house_data.sql' file
# 5. Click 'Go'
```

### Step 3: Update CBIR Features
```bash
python update_cbir_features.py
```

### Step 4: Test the System
```bash
python -c "from cbir_search import search_similar_images; print('CBIR system ready!')"
```

## 📊 Database Structure

### Houses Table
- `h_id`: House ID
- `p_id`: Project ID
- `t_id`: House Type ID
- `h_title`: House Title (Thai)
- `h_description`: House Description (Thai)
- `price`: Price in THB (2M - 15M)
- `bedrooms`: Number of bedrooms (2-6)
- `bathrooms`: Number of bathrooms (1-7)
- `living_area`: Living area in sqm (80-400)
- `parking_space`: Parking spaces (1-3)
- `no_of_floors`: Number of floors (1-3)

### Projects Table
- `p_id`: Project ID
- `p_name`: Project Name (Thai)
- `description`: Project Description
- `address`: Location in Thailand

### House Types Table
- `t_id`: Type ID
- `t_name`: Type Name (Thai)
- `description`: Type Description

### House Features Table
- `f_id`: Feature ID
- `f_name`: Feature Name (Thai)
- `f_description`: Feature Description

## 🎯 Sample Data

### House Names
- บ้านเดี่ยวสไตล์โมเดิร์น
- บ้านสองชั้นคลาสสิก
- บ้านชั้นเดียวสไตล์ไทย
- บ้านวิลล่าสไตล์ยุโรป
- ทาวน์เฮาส์

### Project Names
- โครงการบ้านสวยสุขใจ
- โครงการวิลล่าพาราไดซ์
- โครงการบ้านเดี่ยวหรู
- โครงการทาวน์เฮาส์โมเดิร์น

### Features
- สระว่ายน้ำส่วนตัว
- สวนสวย
- ที่จอดรถ 2 คัน
- ระเบียงกว้าง
- ห้องครัวใหญ่

## 🧪 Testing

After setup, test your CBIR system:

1. **Upload a house image** through your web interface
2. **Check validation** - should work with house images
3. **View search results** - should show many more similar houses
4. **Test different images** - try various house types

## 🔍 Troubleshooting

### MySQL Connection Issues
```bash
# Check if MySQL is running
net start mysql

# Or on Linux/Mac
sudo service mysql start
```

### Import Issues
- Make sure the SQL file is in the correct directory
- Check MySQL user permissions
- Verify database name is 'projectdb'

### CBIR Issues
- Ensure all image files exist in `static/uploads/`
- Check that features directory exists: `static/features/`
- Verify PyTorch and torchvision are installed

## 📈 Expected Results

After setup, your CBIR system should:
- Find 10-20+ similar houses instead of just 2
- Show better similarity scores
- Provide more diverse search results
- Work faster with more data points

## 🎉 Success!

Once setup is complete, your CBIR system will have:
- **50+ houses** to search from
- **Better accuracy** with more data
- **More diverse results** for users
- **Enhanced user experience** with house validation

Your house search system is now ready for production use! 🏠✨
