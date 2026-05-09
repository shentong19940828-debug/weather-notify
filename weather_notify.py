import os                                                                                                                       
  import json                                                                                                                                                                                                                
  import requests                                                                                                                                                                                                            
  from datetime import datetime, timezone, timedelta                                                                                                                                                                         
                                                                                                                                                                                                                             
  # 内置城市坐标库（lon, lat），出差时直接输入城市名即可                                                                                                                                                                     
  CITY_COORDS = {                                                                                                                                                                                                            
      "北京": (116.4074, 39.9042), "上海": (121.4737, 31.2304),                                                                                                                                                              
      "广州": (113.2644, 23.1291), "深圳": (114.0579, 22.5431),                                                                                                                                                              
      "杭州": (120.1551, 30.2741), "南京": (118.7969, 32.0603),                                                                                                                                                              
      "成都": (104.0665, 30.5723), "重庆": (106.5516, 29.5630),                                                                                                                                                              
      "武汉": (114.3054, 30.5931), "西安": (108.9402, 34.3416),                                                                                                                                                              
      "苏州": (120.6196, 31.2990), "天津": (117.1902, 39.1256),                                                                                                                                                              
      "长沙": (112.9388, 28.2278), "郑州": (113.6254, 34.7466),                                                                                                                                                              
      "青岛": (120.3826, 36.0671), "厦门": (118.0894, 24.4798),                                                                                                                                                              
      "宁波": (121.5500, 29.8750), "无锡": (120.3119, 31.4912),                                                                                                                                                              
      "合肥": (117.2272, 31.8206), "福州": (119.2965, 26.0745),                                                                                                                                                              
      "昆明": (102.7123, 25.0406), "济南": (117.1205, 36.6512),                                                                                                                                                              
      "哈尔滨": (126.5358, 45.8028), "沈阳": (123.4315, 41.8057),                                                                                                                                                            
      "大连": (121.6147, 38.9140), "长春": (125.3245, 43.8868),                                                                                                                                                              
      "南昌": (115.8579, 28.6820), "贵阳": (106.7130, 26.5783),                                                                                                                                                              
      "南宁": (108.3665, 22.8170), "海口": (110.3312, 20.0310),                                                                                                                                                              
      "三亚": (109.5119, 18.2523), "珠海": (113.5767, 22.2710),                                                                                                                                                              
      "东莞": (113.7518, 23.0207), "佛山": (113.1220, 23.0219),                                                                                                                                                              
      "温州": (120.6720, 28.0000), "义乌": (120.0751, 29.3063),                                                                                                                                                              
  }                                                                                                                                                                                                                          
                                                                                                                                                                                                                             
  SKYCON_MAP = {                                                                                                                                                                                                             
      "CLEAR_DAY": "晴天", "CLEAR_NIGHT": "晴",             
      "PARTLY_CLOUDY_DAY": "多云", "PARTLY_CLOUDY_NIGHT": "多云",                                                                                                                                                            
      "CLOUDY": "阴天",
      "LIGHT_HAZE": "轻度雾霾", "MODERATE_HAZE": "中度雾霾", "HEAVY_HAZE": "重度雾霾",                                                                                                                                       
      "LIGHT_RAIN": "小雨", "MODERATE_RAIN": "中雨", "HEAVY_RAIN": "大雨", "STORM_RAIN": "暴雨",                                                                                                                             
      "FOG": "大雾",                                                                                                                                                                                                         
      "LIGHT_SNOW": "小雪", "MODERATE_SNOW": "中雪", "HEAVY_SNOW": "大雪", "STORM_SNOW": "暴雪",                                                                                                                             
      "DUST": "浮尘", "SAND": "沙尘", "WIND": "大风",                                                                                                                                                                        
  }                                                                                                                                                                                                                          
                                                                                                                                                                                                                             
  BODY_HEAT_OFFSET = 3                                                                                                                                                                                                       
                                                            
                                                                                                                                                                                                                             
  def resolve_city():                                       
      city = os.environ.get("CITY_OVERRIDE", "").strip()
      if not city:                                                                                                                                                                                                           
          with open("config.json") as f:
              city = json.load(f)["city"]                                                                                                                                                                                    
      if city not in CITY_COORDS:                                                                                                                                                                                            
          raise ValueError(f"城市「{city}」不在内置列表，请联系配置添加坐标")                                                                                                                                                
      lon, lat = CITY_COORDS[city]                                                                                                                                                                                           
      return city, lon, lat                                                                                                                                                                                                  
                                                                                                                                                                                                                             
                                                                                                                                                                                                                             
  def get_weather(lon, lat):                                                                                                                                                                                                 
      token = os.environ["CAIYUN_TOKEN"]                    
      url = f"https://api.caiyunapp.com/v2.6/{token}/{lon},{lat}/daily?dailysteps=1"                                                                                                                                         
      r = requests.get(url, timeout=15)                                                                                                                                                                                      
      r.raise_for_status()                                                                                                                                                                                                   
      daily = r.json()["result"]["daily"]                                                                                                                                                                                    
      aqi_data = daily.get("air_quality", {}).get("aqi", [{}])
      aqi = aqi_data[0].get("max", {}).get("chn") if aqi_data else None                                                                                                                                                      
      return {                                                                                                                                                                                                               
          "temp_max": daily["temperature"][0]["max"],                                                                                                                                                                        
          "temp_min": daily["temperature"][0]["min"],                                                                                                                                                                        
          "rain_prob": daily["precipitation"][0]["probability"],                                                                                                                                                             
          "skycon": daily["skycon"][0]["value"],                                                                                                                                                                             
          "aqi": int(aqi) if aqi else None,                                                                                                                                                                                  
      }                                                     
                                                                                                                                                                                                                             
                                                                                                                                                                                                                             
  def clothing_advice(temp_max, rain_prob):
      ref = temp_max - BODY_HEAT_OFFSET                                                                                                                                                                                      
                                                                                                                                                                                                                             
      if ref < 2:                                                                                                                                                                                                            
          outfit = "羽绒服 + 厚毛衣 + 保暖裤"                                                                                                                                                                                
      elif ref < 8:                                                                                                                                                                                                          
          outfit = "厚棉服/羽绒服 + 毛衣"                                                                                                                                                                                    
      elif ref < 13:                                                                                                                                                                                                         
          outfit = "薄外套 + 长袖（衬衫或卫衣）"                                                                                                                                                                             
      elif ref < 18:                                                                                                                                                                                                         
          outfit = "长袖 T 恤，早晚可带薄外套"              
      elif ref < 23:                                                                                                                                                                                                         
          outfit = "短袖 T 恤"                              
      else:                                                                                                                                                                                                                  
          outfit = "短袖 + 短裤，注意防暑"                  

      if rain_prob >= 0.6:                                                                                                                                                                                                   
          rain_tip = "☔ 今天大概率有雨，务必带伞"
      elif rain_prob >= 0.3:                                                                                                                                                                                                 
          rain_tip = "🌂 有降雨可能，建议备伞"              
      else:                                                                                                                                                                                                                  
          rain_tip = "✅ 降雨概率低，无需带伞"                                                                                                                                                                               
                                                                                                                                                                                                                             
      return outfit, rain_tip                                                                                                                                                                                                
                                                                                                                                                                                                                             
                                                                                                                                                                                                                             
  def aqi_desc(val):                                        
      if val <= 50:   return f"{val} 优"                                                                                                                                                                                     
      if val <= 100:  return f"{val} 良"                                                                                                                                                                                     
      if val <= 150:  return f"{val} 轻度污染"                                                                                                                                                                               
      if val <= 200:  return f"{val} 中度污染"                                                                                                                                                                               
      return f"{val} ⚠️  重度污染，减少外出"                                                                                                                                                                                  
                                                                                                                                                                                                                             
                                                                                                                                                                                                                             
  def push_server_chan(title, content):                                                                                                                                                                                      
      key = os.environ["SERVER_CHAN_KEY"]                                                                                                                                                                                    
      r = requests.post(                                                                                                                                                                                                     
          f"https://sctapi.ftqq.com/{key}.send",
          data={"title": title, "desp": content},                                                                                                                                                                            
          timeout=15,                                                                                                                                                                                                        
      )                                                                                                                                                                                                                      
      result = r.json()                                                                                                                                                                                                      
      print(result)                                                                                                                                                                                                          
      if result.get("data", {}).get("errno", -1) != 0:                                                                                                                                                                       
          raise RuntimeError(f"Server酱推送失败: {result}")                                                                                                                                                                  
                                                                                                                                                                                                                             
                                                                                                                                                                                                                             
  def main():                                                                                                                                                                                                                
      city, lon, lat = resolve_city()                       
      w = get_weather(lon, lat)
      outfit, rain_tip = clothing_advice(w["temp_max"], w["rain_prob"])
                                                                                                                                                                                                                             
      cst = timezone(timedelta(hours=8))                                                                                                                                                                                     
      today = datetime.now(cst).strftime("%m月%d日")                                                                                                                                                                         
      weather_cn = SKYCON_MAP.get(w["skycon"], w["skycon"])                                                                                                                                                                  
      rain_pct = int(w["rain_prob"] * 100)                                                                                                                                                                                   
  
      title = f"🌤️  {city} {today} 天气速报"                                                                                                                                                                                  
                                                            
      aqi_line = f"\n💨 **空气质量**：{aqi_desc(w['aqi'])}" if w["aqi"] else ""                                                                                                                                              
  
      content = f"""\                                                                                                                                                                                                        
  📍 **当前城市：{city}**                                   
                                                                                                                                                                                                                             
  🌡️  **温度**：{w['temp_min']:.0f}°C ~ {w['temp_max']:.0f}°C
  🌤️  **天气**：{weather_cn}                                                                                                                                                                                                  
  🌧️  **降雨概率**：{rain_pct}%{aqi_line}                                                                                                                                                                                     
                                                                                                                                                                                                                             
  ---                                                                                                                                                                                                                        
                                                                                                                                                                                                                             
  👕 **穿衣建议（你的专属版）**                             

  {outfit}

  {rain_tip}
                                                                                                                                                                                                                             
  > 你 BMI≈26，体感比普通人热约3°C，以上建议已自动下调标准
  """                                                                                                                                                                                                                        
                                                            
      push_server_chan(title, content)                                                                                                                                                                                       
      print(f"推送成功：{city}")                            
                                                                                                                                                                                                                             
                                                            
  if __name__ == "__main__":
      main()
