from root import root
from menu import (
	bind_menu,
	test_command_1,
	test_command_2,
)
# 所有的菜单功能都包装在 menu 里面，方便插拔
bind_menu(test_command_1)
bind_menu(test_command_2)



root.mainloop()