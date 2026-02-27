@echo off
echo Setting up KidSpark Database...
echo.
echo Make sure MySQL is running!
echo.
mysql -u root -proot123 < database_setup.sql
echo.
echo Database setup complete!
echo.
pause
