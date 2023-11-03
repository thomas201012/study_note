void lcd(void) {
	if(cfg.flg2.screen_off)
		return;
	bool set_small_number_and_bat = true;

	bool _ble_con =	ble_connected != 0 || (ext_key.rest_adv_int_tad & 2) != 0;
	bool show_ext = lcd_flg.chow_ext_ut >= utc_time_sec;
	if(cfg.flg.show_time_smile || cfg.flg.show_batt_enabled || show_ext)
		lcd_flg.update_next_measure = 0;
	else
		lcd_flg.update_next_measure = 1;
	if (show_ext && (lcd_flg.show_stage & 2)) { // show ext data
		if (lcd_flg.show_stage & 1) { // stage blinking or show battery or clock
			if (cfg.flg.show_batt_enabled
				|| measured_data.battery_level <= 15
				) { // Battery
				show_smiley(0); // stage show battery
				show_battery_symbol(1);
				show_small_number((measured_data.battery_level >= 100) ? 99 : measured_data.battery_level, 1);
				set_small_number_and_bat = false;
			} else if (cfg.flg.show_time_smile) { // show clock
				show_smiley(0); // stage clock/blinking and blinking on
			}
			else
				show_smiley(*((uint8_t *) &ext.flg));
		}
		else
			show_smiley(*((uint8_t *) &ext.flg));
		if (set_small_number_and_bat) {
			show_battery_symbol(ext.flg.battery);
			show_small_number(ext.small_number, ext.flg.percent_on);
		}
		show_temp_symbol(*((uint8_t *) &ext.flg));
		show_big_number_x10(ext.big_number);
	} 
    
    
    else {
		if (lcd_flg.show_stage & 1) { // stage clock/blinking or show battery
			if (cfg.flg.show_batt_enabled|| measured_data.battery_level <= 15
				) { // Battery
				show_smiley(0); // stage show battery
				show_battery_symbol(1);
				show_small_number((measured_data.battery_level >= 100) ? 99 : measured_data.battery_level, 1);
				set_small_number_and_bat = false;
			} else if (cfg.flg.show_time_smile) { // show clock
				show_smiley(0); // stage blinking and blinking on
			} else {
				if (cfg.flg.comfort_smiley) { // comfort on
					show_smiley(is_comfort(measured_data.temp, measured_data.humi));
				} else
					show_smiley(cfg.flg2.smiley);
			}
		} else {
			if (cfg.flg.comfort_smiley) { // comfort on
				show_smiley(is_comfort(measured_data.temp, measured_data.humi));
			} else
				show_smiley(cfg.flg2.smiley);
		}
		if (set_small_number_and_bat) {
			show_battery_symbol(0);
			show_small_number(measured_data.humi_x1, 1);
		}
		if (cfg.flg.temp_F_or_C) {
			show_temp_symbol(TMP_SYM_F); // "°F"
			show_big_number_x10((((measured_data.temp / 5) * 9) + 3200) / 10); // convert C to F
		} else {
			show_temp_symbol(TMP_SYM_C); // "°C"
			show_big_number_x10(measured_data.temp_x01);
		}
	}
	show_ble_symbol(_ble_con);
}