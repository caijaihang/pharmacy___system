/**
 * VicroCode SDK
 * @version v001
 * @releaseDate 2025-10-28
 * @description 让您的项目轻松集成金币扣费功能，用户消费的金币将100%转为您的收益
 * @author VicroCode Team
 * @license MIT
 * 
 * 文件名：vicrocode-sdk-v001.js
 * 下载地址：https://www.vicrocode.com/sdk/vicrocode-sdk-v001.js
 * 
 * 适用场景：
 * - 您的项目在VicroCode平台内运行
 * - 无需密钥管理，开箱即用
 * - 自动通过用户Session验证身份
 * 
 * 使用方法：
 * 1. 下载SDK文件并放入您的项目根目录
 * 2. 在您的项目HTML中引入：<script src="./vicrocode-sdk-v001.js"></script>
 * 3. 在VicroCode项目管理页面启用扣费功能
 * 4. 创建SDK实例并调用charge方法
 * 
 * 示例：
 * const sdk = new VicroCodeSDK({ projectId: 123 });
 * 
 * // 扣费（您自定义金额）
 * const result = await sdk.charge('use_feature', 2, '使用功能');
 * if (result.success) {
 *   console.log('扣费成功！');
 * }
 * 
 * 版本历史：
 * v001 (2025-10-28) - 初始版本，移除API Key/Secret，改用Session验证
 */

(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    // Node.js/CommonJS
    module.exports = factory();
  } else {
    // Browser全局变量
    root.VicroCodeSDK = factory();
  }
}(typeof self !== 'undefined' ? self : this, function() {
  'use strict';

  /**
   * VicroCode SDK 主类（简化版）
   */
  class VicroCodeSDK {
    /**
     * 构造函数
     * @param {Object} config - 配置对象
     * @param {number} [config.projectId] - 您的项目ID（可选，不提供时会自动从URL获取）
     * @param {string} [config.apiBaseUrl=''] - API基础URL（选填，通常无需设置）
     * @param {boolean} [config.debug=false] - 是否开启调试模式（选填）
     */
    constructor(config = {}) {
      // 自动获取项目ID（从URL或配置中）
      this.projectId = config.projectId || this._autoDetectProjectId();
      
      if (!this.projectId) {
        throw new Error('VicroCode SDK 初始化失败：无法获取项目ID，请确保在VicroCode平台内运行或手动提供projectId参数');
      }

      this.apiBaseUrl = config.apiBaseUrl || '';
      this.debug = config.debug || false;

      if (this.debug) {
        console.log('[VicroCode SDK] 初始化成功', {
          projectId: this.projectId,
          apiBaseUrl: this.apiBaseUrl,
          autoDetected: !config.projectId
        });
      }
    }

    /**
     * 自动检测项目ID
     * @private
     * @returns {number|null} 项目ID
     */
    _autoDetectProjectId() {
      try {
        // 方法1：从当前页面URL参数获取
        const urlParams = new URLSearchParams(window.location.search);
        const projectIdFromParam = urlParams.get('projectId');
        if (projectIdFromParam) {
          return parseInt(projectIdFromParam);
        }

        // 方法2：从父窗口URL提取（适用于iframe中运行的项目）
        try {
          const parentUrl = window.parent.location.href;
          // 匹配 /p/数字 格式
          const match = parentUrl.match(/\/p\/(\d+)/);
          if (match && match[1]) {
            return parseInt(match[1]);
          }
        } catch (e) {
          // 跨域情况下无法访问parent.location，忽略此方法
          if (this.debug) {
            console.log('[VicroCode SDK] 无法访问父窗口URL（跨域限制），尝试其他方法');
          }
        }

        // 方法3：从当前页面路径提取
        const currentMatch = window.location.pathname.match(/\/p\/(\d+)/);
        if (currentMatch && currentMatch[1]) {
          return parseInt(currentMatch[1]);
        }

        return null;
      } catch (error) {
        if (this.debug) {
          console.error('[VicroCode SDK] 自动检测项目ID失败:', error);
        }
        return null;
      }
    }

    /**
     * 发送API请求
     * @private
     * @param {string} endpoint - API端点
     * @param {Object} body - 请求体
     * @returns {Promise<Object>} 响应数据
     */
    async _request(endpoint, body = {}) {
      try {
        if (this.debug) {
          console.log('[VicroCode SDK] 发送请求', {
            endpoint: endpoint,
            body: body
          });
        }

        const response = await fetch(`${this.apiBaseUrl}${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(body),
          credentials: 'include' // 携带Cookie（Session）
        });

        const data = await response.json();
        
        if (this.debug) {
          console.log('[VicroCode SDK] 收到响应', {
            status: response.status,
            data: data
          });
        }

        return data;
      } catch (error) {
        console.error('[VicroCode SDK] 请求失败:', error);
        throw error;
      }
    }

    /**
     * 验证用户登录状态
     * @returns {Promise<Object>} 用户信息
     * @example
     * const result = await sdk.verifyUser();
     * if (result.success && result.data.is_logged_in) {
     *   console.log('用户已登录', result.data);
     *   // 用户已登录VicroCode平台，可以继续使用您的功能
     * }
     */
    async verifyUser() {
      return await this._request('/api/charge/verify-user', {});
    }

    /**
     * 扣费接口
     * @param {string} action - 动作名称（用于标识扣费原因，如：'play_game', 'unlock_feature'）
     * @param {number} amount - 扣费金额（金币数量，必须大于0，您可以自定义）
     * @param {string} [description] - 描述信息（可选，默认使用action）
     * @returns {Promise<Object>} 扣费结果
     * @example
     * const result = await sdk.charge('play_game', 2, '开始游戏');
     * if (result.success) {
     *   console.log('扣费成功！用户已支付2金币');
     *   // 执行您的业务逻辑，如开始游戏
     * } else {
     *   console.error('扣费失败：', result.message);
     * }
     */
    async charge(action, amount, description) {
      // 验证金额参数
      if (typeof amount !== 'number' || amount <= 0) {
        throw new Error('扣费金额必须是大于0的数字');
      }
      
      return await this._request('/api/charge/in-project', {
        project_id: this.projectId,
        action: action,
        amount: amount,
        description: description || action
      });
    }

    /**
     * 引导用户登录VicroCode平台
     * @param {string} [redirectUrl] - 登录后重定向的URL（默认返回当前页面）
     * @example
     * sdk.showLoginPrompt();
     * // 用户将跳转到VicroCode登录页面，登录后返回您的项目
     */
    showLoginPrompt(redirectUrl) {
      const loginUrl = `${this.apiBaseUrl}/register-login?redirect=${encodeURIComponent(redirectUrl || window.location.href)}`;
      window.location.href = loginUrl;
    }

    /**
     * 引导用户充值
     * @example
     * sdk.showRechargePrompt();
     * // 用户将跳转到VicroCode充值页面
     */
    showRechargePrompt() {
      window.location.href = `${this.apiBaseUrl}/user-recharge`;
    }

    /**
     * 完整的扣费流程（带用户提示，推荐使用）
     * @param {string} action - 动作名称
     * @param {number} amount - 扣费金额（金币数量，必须大于0，您可以自定义）
     * @param {string} [description] - 描述信息
     * @param {Object} [options] - 选项
     * @param {Function} [options.onSuccess] - 扣费成功回调
     * @param {Function} [options.onFailed] - 扣费失败回调
     * @param {Function} [options.onNotLoggedIn] - 用户未登录回调
     * @param {Function} [options.onInsufficientBalance] - 用户余额不足回调
     * @returns {Promise<Object>} 扣费结果
     * @example
     * await sdk.chargeWithPrompt('play_game', 2, '开始游戏', {
     *   onSuccess: (result) => {
     *     console.log('扣费成功！用户已支付2金币');
     *     // 执行您的业务逻辑，如开始游戏
     *   },
     *   onInsufficientBalance: () => {
     *     alert('用户金币不足，请引导充值！');
     *   }
     * });
     */
    async chargeWithPrompt(action, amount, description, options = {}) {
      // 验证金额参数
      if (typeof amount !== 'number' || amount <= 0) {
        throw new Error('扣费金额必须是大于0的数字');
      }
      
      // 1. 验证用户登录状态
      const userInfo = await this.verifyUser();
      
      if (!userInfo.success || !userInfo.data.is_logged_in) {
        if (options.onNotLoggedIn) {
          options.onNotLoggedIn();
        } else {
          if (confirm('用户尚未登录VicroCode平台，是否引导用户前往登录？')) {
            this.showLoginPrompt();
          }
        }
        return {
          success: false,
          error_code: 'NOT_LOGGED_IN',
          message: '用户未登录'
        };
      }

      // 2. 执行扣费
      const result = await this.charge(action, amount, description);
      
      // 3. 处理结果
      if (result.success) {
        if (options.onSuccess) {
          options.onSuccess(result);
        }
      } else {
        if (result.error_code === 'INSUFFICIENT_BALANCE') {
          if (options.onInsufficientBalance) {
            options.onInsufficientBalance(result);
          } else {
            if (confirm('用户金币余额不足，是否引导用户前往充值？')) {
              this.showRechargePrompt();
            }
          }
        } else {
          if (options.onFailed) {
            options.onFailed(result);
          } else {
            alert('扣费失败：' + result.message);
          }
        }
      }
      
      return result;
    }

    /**
     * 检查用户余额（已废弃）
     * @deprecated 为保护用户隐私，此方法已废弃
     * @param {number} requiredAmount - 需要的金币数量
     * @returns {Promise<boolean>} 总是返回true
     * @example
     * // ❌ 不推荐使用
     * const hasEnough = await sdk.checkBalance(10);
     * 
     * // ✅ 推荐使用 chargeWithPrompt 替代
     * await sdk.chargeWithPrompt('use_feature', 10, '使用功能', {
     *   onSuccess: () => console.log('用户余额充足，扣费成功'),
     *   onInsufficientBalance: () => console.log('用户余额不足')
     * });
     */
    async checkBalance(requiredAmount) {
      // 注意：由于保护用户隐私，无法直接获取用户余额
      // 建议直接使用 chargeWithPrompt 方法，它会自动处理余额不足的情况
      console.warn('[VicroCode SDK] checkBalance方法已废弃，建议使用chargeWithPrompt方法');
      return true; // 总是返回true，让实际的扣费操作来处理余额检查
    }
  }

  // 导出SDK类
  return VicroCodeSDK;
}));
