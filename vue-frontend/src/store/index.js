import { createStore } from 'vuex';

export default createStore({
  state: { user: null, role: null },
  mutations: {
    setUser(state, user) { state.user = user; },
    setRole(state, role) { state.role = role; }
  },
  actions: {
    login({ commit }, { user, role }) { commit('setUser', user); commit('setRole', role); },
    logout({ commit }) { commit('setUser', null); commit('setRole', null); }
  },
  getters: { getUser: state => state.user, getRole: state => state.role }
});
