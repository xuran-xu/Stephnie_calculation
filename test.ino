// 定义引脚
const int SOUND_PIN = 28;     // 声音传感器输入端口 GPI028
const int RED_PIN = 15;       // 红灯输出端口 GPIO15
const int YELLOW_PIN = 16;    // 黄灯输出端口 GPIO16
const int GREEN_PIN = 17;     // 绿灯输出端口 GPIO17

// 定义声音阈值（根据实际环境调整）
const int NOISE_LOW = 45;     // 低噪声阈值 45dB
const int NOISE_MED = 48;     // 中等噪声阈值 48dB
const int NOISE_HIGH = 52;    // 高噪声阈值 52dB（根据传感器规格52-48dB）

// 采样设置
const int SAMPLE_WINDOW = 50;  // 采样窗口时间(ms)
const int SAMPLE_COUNT = 10;   // 采样次数

void setup() {
  // 初始化串口通信，用于调试
  Serial.begin(115200);
  
  // 配置引脚模式
  pinMode(SOUND_PIN, INPUT);
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  
  // 初始化所有LED为关闭状态
  digitalWrite(RED_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);
}

// 获取平均声音级别
int getSoundLevel() {
  long sum = 0;
  
  // 多次采样取平均值，提高准确性
  for(int i = 0; i < SAMPLE_COUNT; i++) {
    sum += analogRead(SOUND_PIN);
    delay(SAMPLE_WINDOW / SAMPLE_COUNT);
  }
  
  int soundLevel = sum / SAMPLE_COUNT;
  
  // 将模拟值映射到分贝范围（根据实际传感器校准）
  // 假设模拟值0-4095映射到40-60分贝
  int dbLevel = map(soundLevel, 0, 4095, 40, 60);
  
  return dbLevel;
}

void updateLEDs(int dbLevel) {
  // 所有LED默认关闭
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(RED_PIN, LOW);
  
  // 根据分贝级别逐级点亮LED
  if(dbLevel >= NOISE_LOW) {
    digitalWrite(GREEN_PIN, HIGH);  // 低噪声，绿灯亮
  }
  if(dbLevel >= NOISE_MED) {
    digitalWrite(YELLOW_PIN, HIGH); // 中等噪声，黄灯亮
  }
  if(dbLevel >= NOISE_HIGH) {
    digitalWrite(RED_PIN, HIGH);    // 高噪声，红灯亮
  }
}

void loop() {
  // 获取当前声音级别
  int dbLevel = getSoundLevel();
  
  // 更新LED显示
  updateLEDs(dbLevel);
  
  // 打印调试信息
  Serial.print("Sound Level (dB): ");
  Serial.println(dbLevel);
  
  // 短暂延时，避免频繁刷新
  delay(100);
}
