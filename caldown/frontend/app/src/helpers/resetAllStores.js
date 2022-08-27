/*
reset all stores
*/

import * as stores from "@/stores";

export const resetAllStores = () => {
    stores.useRecommendationStore().$reset();
    stores.useUsersStore().$reset();
    stores.useAuthStore().$reset();
}